from flask import render_template
from datetime import datetime


def register_views(app):
    app.context_processor(base_context)
    app.add_url_rule('/', view_func=index)


def index():
    return render_template('index.html')


def base_context():
    return {
        "now": datetime.now()
    }
