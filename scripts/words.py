from alphabet_detector import AlphabetDetector
from scipy.sparse import dok_matrix, vstack
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from string import punctuation
import multiprocessing
import numpy as np
import html2text
import nltk
import os


class WordsProcess:
    def __init__(self, folder_path):
        nltk.download('stopwords', quiet=True)
        self.pages = {}
        self.vectors = {}
        self.terms = None
        self.folder_path = os.path.abspath(folder_path)
        self.read_pages()
        self.get_all_terms()

    def all_pages_paths(self):
        return [os.path.join(self.folder_path, filename) for filename in os.listdir(self.folder_path)]

    def read_pages(self):
        with multiprocessing.Pool(processes=8) as pool:
            res = pool.map(WordsProcess.tokenize_file, self.all_pages_paths())
        for key, val in res:
            self.pages[key] = val

    def get_all_terms(self):
        if self.terms is not None:
            return self.terms
        result = set()
        for key, val in self.pages.items():
            result |= set(val)
        self.terms = sorted(list(result))
        return self.terms

    @staticmethod
    def process_word(word):
        ad = AlphabetDetector()
        if not ad.is_latin(word):
            return ''

        banned_fragments = ['.html', 'http://', 'https://', '.jpg', '.svg', '.png']
        for banned in banned_fragments:
            if banned in word:
                return ''

        word = word.lower()
        word = PorterStemmer().stem(word)
        chars = list(punctuation)
        chars = chars + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        chars = chars + ['®']
        for char in chars:
            word = word.replace(char, '')

        stop_words = list(stopwords.words('english'))
        stop_words += ['aa', 'aaa', 'bb', 'bbb']
        for stop in stop_words:
            if stop == word:
                return ''

        if len(set(word)) == 1:
            return ''

        return word

    @staticmethod
    def tokenize_file(path):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_tables = True
        h.ignore_emphasis = True
        with open(path, 'r') as file:
            res = h.handle(file.read()).split()
            res = list(filter(lambda w: len(w) > 1, map(WordsProcess.process_word, res)))
            return path.split('/')[-1], res

    def get_page_vector(self, page):
        result = dok_matrix((len(self.terms), 1))
        words = self.pages[page]
        bag = {}
        for word in words:
            if word in bag:
                bag[word] += 1
            else:
                bag[word] = 1
        for key, val in sorted(bag.items()):
            result[self.terms.index(key)] = val
        return result

    def get_all_vectors(self):
        for page in self.pages.keys():
            self.vectors[page] = self.get_page_vector(page)
        return self.vectors


if __name__ == '__main__':
    folder = '../wiki'
    # folder = '../test_dir'
    proc = WordsProcess(folder)
    proc.get_all_vectors()
