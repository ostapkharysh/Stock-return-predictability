import os
import time

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, Manager, cpu_count


def download_file(args):
    url, out_dir, my_dict = args
    r = requests.get(url)
    html_doc = r.text
    filename = os.path.join(out_dir, url[url.rfind("/") + 1:] + ".html")
    soup = BeautifulSoup(html_doc, 'html.parser')
    tag = soup.select_one(".StandardArticleBody_body")
    not_found = soup.select_one("#sectionTitle")
    if tag != None:
        my_dict[filename] = tag.text
    elif not_found:
        print(url, not_found.text)
    else:
        print(url, "Error")

def retrieve_links(date):
    url = "https://www.reuters.com/resources/archive/us/{}.html".format(date)
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    links = soup.select(".headlineMed a")
    urls2parse = []
    for link in links:
        url = link.get("href")
        if not url.startswith("http://www.reuters.com/news/video/videoStory?storyID="):
            urls2parse.append(url)
    return urls2parse

if __name__ == "__main__":
    cpu_count = cpu_count() * 8
    date = "20140102"
    start = time.time()
    urls2parse = retrieve_links(date)
    out_dir = "../data/" + date
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    manager = Manager()
    my_dict = manager.dict()
    args = [(url, out_dir, my_dict) for url in urls2parse]
    with Pool(cpu_count) as p:
        p.map(download_file, args)
    # print(my_dict)
    d = my_dict._getvalue()
    print(time.time() - start)
    print(len(d), len(urls2parse))
