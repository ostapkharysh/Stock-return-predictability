# SQLALCHEMY
from sqlalchemy import create_engine
from sqlalchemy import inspect, select, MetaData, and_
import datetime
import pandas as pd
import numpy as np

from dateutil.relativedelta import *

start_p = datetime.datetime.strptime("2016-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')  # 2016-02-01
finish_p = datetime.datetime.strptime("2019-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')

step = relativedelta(months=+1)
t = start_p

time_p = list()
while t < finish_p:
    time_p.append(t)
    t += step

for ix in range(len(time_p) - 1):

    db_uri = 'postgresql://ostap:12345@localhost:5432/goog'
    engine = create_engine(db_uri)
    conn = engine.connect()

    inspector = inspect(engine)

    # Get table information

    meta = MetaData(engine, reflect=True)
    table = meta.tables['news']

    select_st = select(
        [table.c.DATE, table.c.TONE, table.c.DOCUMENTIDENTIFIER, table.c.SOURCECOMMONNAME, table.c.GCAM]).where(
        and_(table.c.DATE < str(time_p[ix + 1]), table.c.DATE > str(time_p[ix])))

    res = conn.execute(select_st).fetchall()

    news = dict()
    news['date'] = [datetime.datetime.strptime(el[0], '%Y%m%d%H%M%S') for el in res if '.' not in el[0]]

    sents = [el[1] for el in res if '.' not in el[0]]

    conn.close()

    sent = [x.split(',') for x in sents]

    news['tone'] = [float(el[0]) for el in sent]
    news['positive'] = [float(el[1]) for el in sent]
    news['negative'] = [float(el[2]) for el in sent]
    news['polarity'] = [float(el[3]) for el in sent]
    news['activ_den'] = [float(el[4]) for el in sent]
    news['self_den'] = [float(el[5]) for el in sent]

    news['source'] = [el[2] for el in res if '.' not in el[0]]
    news['agency'] = [el[3] for el in res if '.' not in el[0]]
    news['words'] = [el[4] for el in res if '.' not in el[0]]

    del res

    TONE = pd.DataFrame.from_dict(news)

    print("TONE LOADED...")

    TONE = TONE.sort_values(by=['date'])
    TONE = TONE[
        ['date', 'tone', 'positive', 'negative', 'polarity', 'activ_den', 'self_den', 'source', 'agency', 'words']]
    TONE = TONE.reset_index(drop=True)
    print(TONE.head())

    intraday = pd.DataFrame(columns=['date', 'price'])

    with open("additional_data/202_googl.txt", "r") as stock:
        for line in stock:
            el = line.split(" ")[0] + " " + line.split(" ")[1]
            data = datetime.datetime.strptime(line.split(" ")[0] + " " + line.split(" ")[1], '%Y-%m-%d %H:%M:%S')
            intraday = intraday.append({'date': data, 'price': float(line.split(" ")[-1].strip())}, ignore_index=True)

    period_df = intraday[
        (intraday['date'] >= str(time_p[ix + 1])) & (intraday['date'] < str(time_p[ix + 1]))]  # '2016-01-31 23:45:00'
    period_df['date'] = pd.to_datetime(period_df['date'])

    start = time_p[ix]  # datetime.datetime.strptime("2016-01-01 00:00:00", '%Y-%m-%d %H:%M:%S') #2016-02-01
    finish = time_p[ix + 1]  # datetime.datetime.strptime("2016-02-01 00:00:00", '%Y-%m-%d %H:%M:%S')

    step = datetime.timedelta(minutes=15)
    t = start

    time = list()
    while t < finish:
        time.append(t)
        t += step

    period_df = period_df[pd.to_datetime(period_df['date'].values).minute % 15 == 0]
    period_df = period_df.reset_index(drop=True)

    lack_p = set(time) - set(period_df['date'])

    for el in lack_p:
        period_df = period_df.append({'date': el, 'price': np.nan}, ignore_index=True)

    lack_t = set(time) - set(TONE['date'])
    for el in lack_t:
        TONE = TONE.append({'date': el, 'tone': np.nan, 'positive': np.nan,
                            'negative': np.nan, 'polarity': np.nan,
                            'activ_den': np.nan,
                            'self_den': np.nan}, ignore_index=True)

    period_df = period_df.sort_values(by=['date'])
    TONE = TONE.sort_values(by=['date'])

    period_df = period_df.reset_index(drop=True)
    TONE = TONE.reset_index(drop=True)

    TONE['price'] = TONE[['date']].merge(period_df, how='left').price

    from collections import Counter

    agency = dict(Counter(TONE.agency))
    agencies_lst = list(agency.items())

    ton = TONE[['tone', 'positive', 'negative', 'polarity', 'activ_den', 'self_den'
        , 'agency', 'price']].copy()

    ton_ag = sorted(agencies_lst, key=lambda x: x[1], reverse=True)

    TOP_tones = pd.DataFrame({'date': [], 'price': []})

    TOP_tones['date'] = TONE.date.unique()
    TOP_tones['price'] = TOP_tones[['date']].merge(period_df, how='left').price

    for el in ton_ag[:100]:
        temp = pd.DataFrame({'date': TONE.date.unique(), 'agency': [el[0]] * len(TONE.date.unique()), el[0]: None})
        temp[el[0]] = temp[['date', 'agency']].merge(TONE, how='left').tone
        TOP_tones[el[0]] = temp[el[0]]

    prc = TOP_tones[TOP_tones.price.notnull()]

    entity = list(prc.columns)[2:]  # omit date and price
    correlations = list(prc.corr()['price'])[1:]  # omit price
    lst = [[entity[x], correlations[x]] for x in range(len(correlations))]

    companies = sorted(lst, key=lambda x: x[1], reverse=True)
    sel_companies = [el[0] for el in companies]  # NO FILTER BY PEARSON CORRELATION
    # sel_companies = [el[0] for el in companies if abs(el[1]) >= 0.20]

    most_TONE = TONE[TONE.agency.isin(sel_companies)]  # 1 FILTER

    GCAM_most = ['c18.59', 'c18.60', 'c18.61', 'c18.63', 'c18.154', 'c18.286', 'c18.287', 'c18.288']

    fin = list()
    for el in most_TONE.words:
        dec = False
        for tp in GCAM_most:
            if tp in el:
                dec = True
        fin.append(dec)
    most_TONE['financial'] = fin

    most_TONE = most_TONE[most_TONE.financial == True]

    most_TONE = most_TONE[most_TONE.price.notnull()]

    most_TONE = most_TONE.reset_index(drop=True)

    most_TONE.to_csv('testDATA/' + str(start_p).split(" ")[0] + '.csv')

    print("DONE:" + str(start_p).split(" ")[0])
