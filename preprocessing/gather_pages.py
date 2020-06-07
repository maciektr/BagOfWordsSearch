from bs4 import BeautifulSoup
import multiprocessing
import urllib.request
import requests
import os

from search_web.models import db
from search_web.models.article import Article


class GatherPages:
    _N_PROC = 8
    folder = ''

    def __init__(self, folder):
        GatherPages.folder = folder
        self.pages_url = []

    @staticmethod
    def filter_urls_cond(text):
        return text is not None \
               and ('wiki' in text) \
               and (':' not in text) \
               and ('.' not in text) \
               and ('#' not in text)

    @staticmethod
    def get_all_urls(url):
        page_content = requests.get(url).content
        res = []
        soup = BeautifulSoup(page_content, "html.parser")
        for link in soup.findAll('a'):
            res.append(link.get('href'))
        res = list(set(filter(GatherPages.filter_urls_cond, res)))
        return res

    @staticmethod
    def flatten(arr):
        res = []
        for sub_arr in arr:
            for value in sub_arr:
                res.append(value)
        return res

    @staticmethod
    def save_page(url):
        file_name = GatherPages.folder + '/' + url.split('/')[-1] + '.html'
        if os.path.exists(file_name):
            return

        if url[:5] == '/wiki':
            url = 'https://en.wikipedia.org' + url

        art = Article(url=url, local_path=file_name, title=url.split('/')[-1])
        db.session.add(art)
        db.session.commit()

        page = urllib.request.urlopen(url).read()
        print('Downloading:', file_name)
        with open(file_name, 'wb') as file:
            file.write(page)

    def load_from_sources(self, sources):
        with multiprocessing.Pool(processes=GatherPages._N_PROC) as pool:
            res = pool.map(GatherPages.get_all_urls, sources)
            self.pages_url += list(set(GatherPages.flatten(res)))
            pool.map(GatherPages.save_page, self.pages_url)
