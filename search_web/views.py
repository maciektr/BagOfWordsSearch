from flask import current_app, request, render_template
from datetime import datetime


def register_views(app):
    app.context_processor(base_context)
    app.add_url_rule('/', view_func=index)
    app.add_url_rule('/search/', view_func=search, methods=['POST'])


def index():
    return render_template('index.html')


def search():
    query = request.form['query']
    print('Query:', query)
    print(current_app.search(query))
    return render_template('index.html')


def base_context():
    return {
        "now": datetime.now()
    }
