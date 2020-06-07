from bs4 import BeautifulSoup
import multiprocessing
import urllib.request
import requests
import os


class GatherPages:
    _N_PROC = 8
    folder = ''

    def __init__(self):
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

        url = 'https://en.wikipedia.org' + url
        page = urllib.request.urlopen(url).read()
        print('Downloading:', file_name)
        with open(file_name, 'wb') as file:
            file.write(page)

    def load_from_sources(self, sources):
        with multiprocessing.Pool(processes=GatherPages._N_PROC) as pool:
            res = pool.map(GatherPages.get_all_urls, sources)
            self.pages_url += list(set(GatherPages.flatten(res)))
            pool.map(GatherPages.save_page, self.pages_url)
