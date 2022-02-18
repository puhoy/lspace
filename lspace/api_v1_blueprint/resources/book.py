from flask_restx import Resource
from flask_restx._http import HTTPStatus

from lspace.api_v1_blueprint import api
from lspace.api_v1_blueprint.models import BookSchema, PaginatedBookSchema
from lspace.api_v1_blueprint.resource_helpers import get_pagination_args_parser, \
    add_fields_to_parser, run_query
from lspace.models import Book, Shelf, Author

filter_fields = ['title', 'publisher', 'shelf', 'author', 'md5sum', 'language', 'year']

args_parser = get_pagination_args_parser()
add_fields_to_parser(args_parser, filter_fields)


def filter_by_shelf(value):
    if value == 'default':
        return Book.shelf == None
    else:
        return Book.shelf.has(Shelf.name.ilike(value))


def filter_by_author(value):
    if value == 'None':
        return Book.authors == None
    else:
        return Book.authors.any(Author.name.ilike(value))


def default_filter(key, value):
    if value in ['None', ]:
        return getattr(Book, key) == None
    return getattr(Book, key).ilike(value)


filter_map = {
    'shelf': filter_by_shelf,
    'author': filter_by_author,
    '__default': default_filter
}


class BookCollection(Resource):

    @api.expect(args_parser, validate=True)
    @api.response(200, "OK")
    def get(self):
        args = args_parser.parse_args()
        page = args.pop('page')
        per_page = args.pop('per_page')
        query = run_query(Book, args, filter_map, page, per_page)
        return PaginatedBookSchema().dump(query), HTTPStatus.OK


class BookItem(Resource):
    @api.response(200, "OK")
    def get(self, id, **kwargs):
        book = Book.query.get(id)
        return BookSchema().dump(book), HTTPStatus.OK
