from search_web.models import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import text


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    url = db.Column(db.String(2048), unique=True, nullable=False)
    local_path = db.Column(db.String(2048), unique=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
