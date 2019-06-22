from flask_restplus import Resource, reqparse
from sqlalchemy import func

from lspace.api_blueprint import api
from lspace.api_blueprint.models import book_model, get_paginated_model, pagination_arguments
from lspace.models import Book


def get_filters(*fields):
    filter_fields = reqparse.RequestParser()
    for field in fields:
        filter_fields.add_argument(field, type=str, required=False, store_missing=False)
    return filter_fields


book_filters = get_filters('title', 'publisher')





@api.route('/books/')
class BookCollection(Resource):

    @api.expect(book_filters, validate=True)
    @api.expect(pagination_arguments, validate=True)
    @api.marshal_with(get_paginated_model(book_model))
    def get(self, **kwargs):
        args = pagination_arguments.parse_args()
        filter_args = book_filters.parse_args()

        q = Book.query

        lower_filters = []
        for k, v in filter_args.items():
            lower_filters.append(func.lower(getattr(Book, k)) == (func.lower(v)))

        q = q.filter(*lower_filters)

        return q.paginate(page=args['page'], per_page=args['per_page'], error_out=False)



@api.route('/books/<int:id>')
class BookItem(Resource):

    @api.marshal_with(book_model, envelope='resource')
    def get(self, id, **kwargs):
        return Book.query.get(id)
