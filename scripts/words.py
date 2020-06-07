from alphabet_detector import AlphabetDetector
from scipy.sparse import lil_matrix, hstack
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
        self.vectors = None
        self.matrix = None
        self.term_id = {}
        self.terms = None
        self.folder_path = os.path.abspath(folder_path)
        self.read_pages()
        self.get_all_terms()
        self._N_PAGES_TO_RET = 5

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

    def calc_term_index(self):
        terms = sorted(self.get_all_terms())
        for i in range(len(terms)):
            self.term_id[terms[i]] = i

    def get_vector_from_words(self, words):
        result = lil_matrix((len(self.terms), 1))
        bag = {}
        for word in words:
            if word in bag:
                bag[word] += 1
            else:
                bag[word] = 1
        for key, val in sorted(bag.items()):
            if key not in self.term_id:
                if key not in self.terms:
                    continue
                self.term_id[key] = self.terms.index(key)
            result[self.term_id[key]] = val
        return result

    def get_page_vector(self, page):
        words = self.pages[page]
        return page, self.get_vector_from_words(words)

    def get_all_vectors(self):
        if self.vectors is not None:
             return self.vectors
        self.vectors = {}
        with multiprocessing.Pool(processes=8) as pool:
            res = pool.map(self.get_page_vector, self.pages.keys())
        for page, vect in res:
            self.vectors[page] = vect
        return self.vectors

    def stack_vectors(self):
        if self.vectors is None:
            self.get_all_vectors()
        vectors = [val for key, val in sorted(self.vectors.items(), key=lambda x:x[0])]
        return hstack(vectors)

    def idf_norm(self, matrix):
        n_docs = len(self.pages.keys())
        idf = np.log(n_docs / np.sum(matrix > 0, axis=1))
        idf_mat = np.array([idf, ] * matrix.shape[1]).T
        return matrix * idf_mat

    def get_matrix(self):
        if self.matrix is not None:
            return self.matrix
        self.matrix = lil_matrix(self.stack_vectors()).toarray()
        self.matrix = self.idf_norm(self.matrix)
        return self.matrix

    def get_all_pages(self):
        return sorted(self.pages.keys())

    def get_bag_from_queries(self, query):
        words = list(filter(lambda w: len(w) > 1, map(WordsProcess.process_word, query.split())))
        return self.get_vector_from_words(words)

    @staticmethod
    def norm(matrix):
        return matrix / np.linalg.norm(matrix, axis=0)

    def search(self, query, n_pages=5):
        query = WordsProcess.norm(self.get_bag_from_queries(query).toarray())
        self.matrix = WordsProcess.norm(self.get_matrix())
        correlation = []
        for col in range(self.matrix.shape[1]):
            print("Dot", np.sum(np.dot(self.matrix[:, col], query)))
            correlation.append(np.dot(self.matrix[:, col], query)[0])
            # print(self.matrix[:, col])
            # print(query)
        # correlation = [np.dot(np.array(self.matrix[:, col]), query) for col in range(self.matrix.shape[1])]
        print(correlation)

        # ids = np.argpartition(correlation, -self._N_PAGES_TO_RET)[-self._N_PAGES_TO_RET:]
        ids = np.argpartition(correlation, -n_pages)[-n_pages:]
        pages = self.get_all_pages()
        return [pages[i] for i in ids]


if __name__ == '__main__':
    # folder = '../wiki'
    # folder = '../tiny2'
    folder = '../test_dir'
    proc = WordsProcess(folder)

    # print(proc.get_all_terms())
    # vect = proc.get_all_vectors()
    # for k,v in vect.items():
    #     print("V", k, '\n', v)

    # print("Matrix")
    # print(proc.get_matrix())
    # print(proc.get_matrix().shape)
    # print(proc.get_bag_from_queries("Panno Litwo"))

    print(proc.search("four wheel drive", n_pages=5))

    # _, a = proc.get_page_vector('Asian_Century')
    # print(np.sum(a), a)
    # print('----------')
    # print(proc.get_all_vectors())
    # print('----------')
    # print(np.sum(proc.vectors['Asian_Century']), proc.vectors['Asian_Century'])
