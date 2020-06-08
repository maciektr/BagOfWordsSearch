from alphabet_detector import AlphabetDetector
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from string import punctuation
import html2text
import nltk


class WordsProcess:
    def __init__(self):
        nltk.download('stopwords', quiet=True)

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
    def tokenize_file(article):
        path = article.local_path
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_tables = True
        h.ignore_emphasis = True
        with open(path, 'r') as file:
            res = h.handle(file.read()).split()
            res = list(filter(lambda w: len(w) > 1, map(WordsProcess.process_word, res)))
            # return path.split('/')[-1], res
            return article.id, res
