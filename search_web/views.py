from flask import current_app, request, render_template
from datetime import datetime

from search_web.models.article import Article


def register_views(app):
    app.context_processor(base_context)
    app.add_url_rule('/', view_func=index)
    app.add_url_rule('/search/', view_func=search, methods=['POST'])


def index():
    return render_template('index.html')


def search():
    query = request.form['query']
    print('Query:', query)
    search_res = list(sorted(current_app.search(query), key=lambda res: res[0]))
    print('Found: ', search_res)
    titles = [t for t, _ in search_res]
    correlations = [c for _, c in search_res]
    articles = list(sorted(Article.query.filter(Article.title.in_(titles)).all(), key=lambda art: art.title))
    search_res = list(sorted(list(filter(lambda x: x[1] > 0, zip(articles, correlations))), key=lambda x: -x[1]))
    return render_template('result.html', search_res=search_res, asked=query)


def base_context():
    return {
        "now": datetime.now()
    }
