from alphabet_detector import AlphabetDetector
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from string import punctuation
import multiprocessing
import html2text
import nltk
import os


def tokenize_file(path):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_tables = True
    h.ignore_emphasis = True
    with open(path, 'r') as file:
        return set(h.handle(file.read()).split())


def get_all_words(folder_path):
    path = os.path.abspath(folder_path)
    with multiprocessing.Pool(processes=8) as pool:
        res = pool.map(tokenize_file, [os.path.join(path, filename) for filename in os.listdir(path)])
    result = set()
    for r in res:
        result = result | r
    return list(result)


def process_word(word):
    ad = AlphabetDetector()
    if not ad.is_latin(word):
        return ''

    banned_fragments = ['.html', 'http://', '.jpg', '.svg', '.png']
    for banned in banned_fragments:
        if banned in word:
            return ''

    word = word.lower()
    word = PorterStemmer().stem(word)
    chars = list(punctuation)
    chars = chars + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
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


def process_words(words):
    nltk.download('stopwords')
    with multiprocessing.Pool(processes=8) as pool:
        words = pool.map(process_word, words)
    words = list(filter(lambda w: len(w) > 1, list(set(words))))
    return list(words)


if __name__ == '__main__':
    # folder = 'wiki'
    folder = 'test_dir'
    res = get_all_words(folder)
    # words = sorted(process_words(res))
    words = process_words(res)
    print("---------")
    # print(words)
    print(len(res))
    print(len(words))
