import flask
from flask import Blueprint, current_app
from flask import render_template

from lspace import db
from lspace.api_v1_blueprint.resource_helpers import run_query
from lspace.models import Book, Author, Shelf

from lspace.api_v1_blueprint.resources.author import filter_map as author_filter_map
from lspace.api_v1_blueprint.resources.book import filter_map as book_filter_map, filter_fields as book_filter_fields
from lspace.api_v1_blueprint.resources.shelf import filter_map as shelf_filter_map
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import request
frontend_blueprint = Blueprint('frontend', __name__, template_folder='templates', static_folder='static')


class BookQueryForm(FlaskForm):
    class meta():
        csrf = False
    title = StringField('title', validators=[])
    author = StringField('author', validators=[])
    publisher = StringField('publisher', validators=[])
    language = StringField('language', validators=[])
    shelf = StringField('shelf', validators=[])
    year = StringField('year', validators=[])

@frontend_blueprint.route('/', methods=['GET', 'POST'])
@frontend_blueprint.route('/books', methods=['GET', 'POST'])
def books():
    page = int(request.args.get('page', 1))
    per_page = 10

    book_args = {}
    form = BookQueryForm()

    for field in book_filter_fields:
        value = request.args.get(field, None)
        if value:
            book_args[field] = value
            getattr(form, field).data = value

    paginated_books = run_query(Book, book_args, book_filter_map, page, per_page)

    return render_template("books.html.jinja2", paginated_books=paginated_books, form=form)


