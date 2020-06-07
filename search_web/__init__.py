from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from preprocessing.preproc_manager import PreprocessingManager
from search_web.views import register_views
from search_web.models import db
from search_web.models.article import Article


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config.from_pyfile('../config.py', silent=True)
    app.secret_key = app.config.get("KEY_SIGNING_SECRET")
    app.static_url_path = app.config.get('STATIC_FOLDER')
    app.static_folder = app.root_path + app.static_url_path

    db.init_app(app)
    app.app_context().push()
    db.create_all()

    PreprocessingManager(app)
    register_views(app)

    admin = Admin(app, name='Search admin', template_mode='bootstrap3')
    admin.add_view(ModelView(Article, db.session))

    return app
