import pandas as pd
import os, sys, csv
import re
import numpy as np
import datetime

from bs4 import BeautifulSoup as BS
import requests
from requests.exceptions import HTTPError, MissingSchema, TooManyRedirects
from requests.exceptions import ConnectionError

from manager import *
from manager import add_company, add_news

from multiprocessing import Pool, cpu_count
from functools import partial

requests.adapters.DEFAULT_RETRIES = 5
csv.field_size_limit(sys.maxsize)


def get_text(link):
    start = datetime.datetime.now()
    try:
        while (datetime.datetime.now() - start).seconds < 4:
            session = requests.Session()
            session.max_redirects = 5
            r = session.get(link, verify=False)
            soup = BS(r.content, 'html.parser')
            if soup.html.title:
                head = soup.html.title.string.strip().lower()
                if "|" in head:
                    head = head.split("|")[0]
                return head
            else:
                return " ".join(link.split('/')[-1].split("-"))
        print("LONG EXECUTION")
        return " ".join(link.split('/')[-1].split("-"))

    except AttributeError:
        print("No article found by this link!", link)
        return " ".join(link.split('/')[-1].split("-"))
    except MissingSchema:
        print('invalid url {} '.format(link))
        return " ".join(link.split('/')[-1].split("-"))
    except TooManyRedirects:
        print('To many redirects')
        return " ".join(link.split('/')[-1].split("-"))
    except ConnectionError as e:
        print(e)
        return " ".join(link.split('/')[-1].split("-"))
    except Exception:
        return " ".join(link.split('/')[-1].split("-"))


def store(news, cp_idx_title):
    news['comp_index'] = cp_idx_title[0]
    if cp_idx_title[1]:
        news['TITLE'] = get_text(news['V2DOCUMENTIDENTIFIER'])
    add_news(news)


def filter_and_store_newsdata(comp_index, start_date, finish_date):

    count = 0

    startDT = datetime.datetime.now()
    print("STARTING SCRIPT: {}".format(str(startDT)))

    total_news = 0
    directory = "//media/ostapkharysh/SP_PHD_U3/gdelt"

    time_periods = sorted(os.listdir(directory))
    print(len(sorted(time_periods)))
    start_doc, finish_doc = start_date + '.gkg.csv', finish_date + '.gkg.csv'
    selected_period = time_periods[time_periods.index(start_doc):time_periods.index(finish_doc) + 1]

    companies = pd.read_csv('additional_data/SnP500Top10.csv')
    selected_company = companies.loc[companies['index'] == comp_index]
    affiliates = [re.sub('[!@#$.]', '', el.lower().lstrip(' ').replace(' ', '-'))
                  for el in selected_company['affiliate'].values[0].split(',')]

    print(selected_period)
    print(affiliates)

    # ADDING COMPANY
    add_company(comp_index)

    for per in selected_period:
        try:
            data = pd.read_csv(directory + '/' + per, delimiter='\t', header=None, encoding='latin-1', engine='python')
        except Exception:
            print("EXCP {}".format(per))
            continue

        filtered_data = data[[1, 2, 3, 4, 9, 13, 15, 17, 23]]
        filtered_data.columns = ['V2.1DATE', 'V2SOURCECOLLECTIONIDENTIFIER', 'V2SOURCECOMMONNAME',
                                 'V2DOCUMENTIDENTIFIER', 'V1LOCATIONS',
                                 'V1ORGANIZATIONS', 'V1.5TONE', 'V2GCAM', 'V2.1ALLNAMES']

        pd.options.mode.chained_assignment = None
        filtered_data['TITLE'] = np.nan

        # ALLNAMES : VERY BROAD SPECIFICATION OF NAME
        # ORGANIZATIONS: MORE PRECISE SPECIFICATION OF NAME

        # DECIDED TO MOVE WITH ONLY "AFF" APPEAREANce IN ALLNAMES AND ORGANIZATIONS

        important_news = list()

        for aff in affiliates:
            for idx, el in enumerate(filtered_data['V2DOCUMENTIDENTIFIER']):

                decision = False
                all_names = False
                organizations = False

                if filtered_data['V2SOURCECOLLECTIONIDENTIFIER'][idx] == 1:

                    if aff in str(el):
                        decision = True
                    if aff in str(filtered_data['V2.1ALLNAMES'][idx]).lower():
                        filtered_data['V2.1ALLNAMES'][idx] = aff
                        all_names = True
                    if aff in str(filtered_data['V1ORGANIZATIONS'][idx]).lower():
                        filtered_data['V1ORGANIZATIONS'][idx] = aff
                        organizations = True

                if decision or all_names or organizations:

                    # Reducing the size of values
                    if len(filtered_data['V2GCAM'][idx]) > 25000:
                        print('V2GCAM to large!')
                        count += 1
                    filtered_data['V2GCAM'][idx] = filtered_data['V2GCAM'][idx][:29950] + '...' \
                        if len(filtered_data['V2GCAM'][idx]) > 30000 else filtered_data['V2GCAM'][idx]
                    if len(str(filtered_data['TITLE'][idx])) > 1499:
                        print('TITLE to large!')
                        count += 1
                    filtered_data['TITLE'][idx] = filtered_data['TITLE'][idx][:1450] + '...' \
                        if len(str(filtered_data['TITLE'][idx])) > 1500 else filtered_data['TITLE'][idx]

                    # Value optimisation
                    if not organizations:
                        filtered_data['V1ORGANIZATIONS'][idx] = None
                    if not all_names:
                        filtered_data['V2.1ALLNAMES'][idx] = None
                    important_news.append(filtered_data.iloc[idx])
                else:
                    pass

        pool = Pool(processes=cpu_count())

        infer = partial(store, cp_idx_title=[comp_index, True])

        pool.map(infer, important_news)
        pool.close()
        pool.join()

        total_news += len(important_news)

        print("FINISHED PERIOD: {}, ADDED {} NEWS".format(per.split(".")[0], len(important_news)))
    print("FINISHED AT: {}".format(str(datetime.datetime.now() - startDT)))
    print("TOTAL NEWS ADDED: {}".format(total_news))
    print(count)


# '20160104220000'
filter_and_store_newsdata('GOOG', '20160101091500', '20190101000000')
#20160101091500