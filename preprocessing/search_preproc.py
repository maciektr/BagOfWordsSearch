from scipy.sparse import lil_matrix, hstack
import multiprocessing
import numpy as np
import os

from search_web.models import db
from search_web.models.article import Article
from .words import WordsProcess


class SearchPreprocessing:
    folder_path = ''

    def __init__(self, folder_path):
        SearchPreprocessing.folder_path = folder_path

        self.pages = {}
        self.vectors = None
        self.matrix = None
        self.term_id = {}
        self.terms = None

    def all_articles(self):
        return Article.query.order_by(Article.title).all()

    def all_pages_paths(self):
        return list(map(lambda art: art.local_path, self.all_articles()))

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
        query = SearchPreprocessing.norm(self.get_bag_from_queries(query).toarray())
        self.matrix = SearchPreprocessing.norm(self.get_matrix())
        correlation = []
        for col in range(self.matrix.shape[1]):
            correlation.append(np.dot(self.matrix[:, col], query)[0])
            # print(self.matrix[:, col])
            # print(query)
        # correlation = [np.dot(np.array(self.matrix[:, col]), query) for col in range(self.matrix.shape[1])]
        # print(correlation)

        # ids = np.argpartition(correlation, -self._N_PAGES_TO_RET)[-self._N_PAGES_TO_RET:]
        ids = np.argpartition(correlation, -n_pages)[-n_pages:]
        pages = self.get_all_pages()
        return [pages[i] for i in ids]
