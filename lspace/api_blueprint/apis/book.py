from flask_restplus import Resource, reqparse
from sqlalchemy import func

from lspace.api_blueprint import api
from lspace.api_blueprint.models import book_model, get_paginated_model, pagination_arguments, get_filters
from lspace.models import Book, Shelve, Author

book_filters = get_filters('title', 'publisher', 'shelve', 'author')


def alchemy_filter(query, filter_args, filter_map):

    filters = []

    for key, value in filter_args.items():
        if key in filter_map.keys():
            filters.append(filter_map[key](value))
        else:
            filters.append(func.lower(getattr(Book, key)) == (func.lower(value)))

    return query.filter(*filters)


@api.route('/books/')
class BookCollection(Resource):

    @api.expect(book_filters, validate=True)
    @api.expect(pagination_arguments, validate=True)
    @api.marshal_with(get_paginated_model(book_model))
    def get(self, **kwargs):
        args = pagination_arguments.parse_args()
        filter_args = book_filters.parse_args()

        q = Book.query

        filter_map = {
            'shelve': Shelve.name.__eq__,
            'author': lambda x: Book.authors.any(func.lower(Author.name) == func.lower(x))
        }

        q = alchemy_filter(q, filter_args, filter_map)

        return q.paginate(page=args['page'], per_page=args['per_page'], error_out=False)


@api.route('/books/<int:id>')
class BookItem(Resource):

    @api.marshal_with(book_model, envelope='resource')
    def get(self, id, **kwargs):
        return Book.query.get(id)
