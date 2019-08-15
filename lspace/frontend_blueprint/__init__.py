from flask import Blueprint
from flask import render_template
from flask import request
from flask_wtf import FlaskForm
from typing import Dict
from wtforms import StringField

from lspace.api_v1_blueprint.resource_helpers import run_query
from lspace.api_v1_blueprint.resources.book import filter_map as book_filter_map, filter_fields as book_filter_fields
from lspace.models import Book

frontend_blueprint = Blueprint('frontend', __name__, template_folder='templates', static_folder='static')


class BookQueryForm(FlaskForm):
    class Meta():
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

    # set up vars for import string
    import_vars = dict()
    for k, v in  dict(**request.args).items():
        if v:
            import_vars[k] = v
    import_vars.pop('page', None)
    import_vars.pop('per_page', None)
    return render_template("books.html.jinja2", paginated_books=paginated_books, form=form, import_vars=import_vars)
