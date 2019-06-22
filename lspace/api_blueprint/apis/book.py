from flask_restplus import Resource

from lspace.api_blueprint import api
from lspace.api_blueprint.models import book_model, get_paginated_model, pagination_arguments
from lspace.models import Book


@api.route('/books/')
class BookCollection(Resource):

    @api.expect(pagination_arguments, validate=True)
    @api.marshal_with(get_paginated_model(book_model))
    def get(self, **kwargs):
        args = pagination_arguments.parse_args()
        return Book.query.paginate(page=args['page'], per_page=args['per_page'], error_out=False)


@api.route('/books/<int:id>')
class BookItem(Resource):

    @api.marshal_with(book_model, envelope='resource')
    def get(self, id, **kwargs):
        return Book.query.get(id)
