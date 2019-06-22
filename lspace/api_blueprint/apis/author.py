from flask_restplus import Resource

from lspace.api_blueprint import api
from lspace.api_blueprint.apis.book import get_paginated_model
from lspace.api_blueprint.models import author_with_books_model, pagination_arguments
from lspace.models import Author


@api.route('/authors/')
class AuthorCollection(Resource):

    @api.expect(pagination_arguments, validate=True)
    @api.marshal_with(get_paginated_model(author_with_books_model))
    def get(self, **kwargs):
        args = pagination_arguments.parse_args()
        return Author.query.paginate(page=args['page'], per_page=args['per_page'], error_out=False)


@api.route('/authors/<int:id>')
class AuthorItem(Resource):

    @api.marshal_with(author_with_books_model, envelope='resource')
    def get(self, id, **kwargs):
        return Author.query.get(id)
