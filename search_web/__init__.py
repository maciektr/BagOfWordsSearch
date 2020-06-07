from flask import Flask

from search_web.views import register_views
from preprocessing.preproc_manager import PreprocessingManager


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py', silent=True)
    app.static_url_path = app.config.get('STATIC_FOLDER')
    app.static_folder = app.root_path + app.static_url_path

    PreprocessingManager(app)
    register_views(app)

    return app