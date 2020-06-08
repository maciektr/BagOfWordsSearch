import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

STATIC_FOLDER = "/static"
FLASK_ADMIN_SWATCH = 'cerulean'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'search_web/appdb.db')
KEY_SIGNING_SECRET = os.getenv("SIGNING_SECRET",
                               'SIGNING-SECRET')


PAGES_FOLDER = 'wiki_pages'
# Loads all pages linked in pages listed below
PAGES_SOURCE = [
    # Cars by make
    # 'https://en.wikipedia.org/wiki/List_of_Kia_Motors_automobiles',
    'https://en.wikipedia.org/wiki/List_of_Toyota_vehicles',
    # 'https://en.wikipedia.org/wiki/List_of_Lexus_vehicles',
    # Countries
    # 'https://simple.wikipedia.org/wiki/Elon_Musk',
    # 'https://simple.wikipedia.org/wiki/Bill_Gates',
]
