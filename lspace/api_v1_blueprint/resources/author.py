from flask_restplus import Resource
from flask_restplus._http import HTTPStatus

from lspace.api_v1_blueprint import api
from lspace.api_v1_blueprint.models import AuthorWithBooksSchema, PaginatedAuthorWithBooksSchema
from lspace.api_v1_blueprint.resource_helpers import get_pagination_args_parser, \
    add_fields_to_parser, \
    apply_filter_map, get_swagger_model
from lspace.models import Book, Author

filter_fields = ['name']

args_parser = get_pagination_args_parser()
add_fields_to_parser(args_parser, filter_fields)

filter_map = {
    'books': lambda value: Author.books.any(Book.title.ilike(value)),
    '__default': lambda key, value: getattr(Author, key).ilike(value)
}


class AuthorCollection(Resource):
    @api.expect(args_parser, validate=True)
    @api.response(200, "OK", get_swagger_model(api, PaginatedAuthorWithBooksSchema))
    def get(self):
        args = args_parser.parse_args()
        page = args.pop('page')
        per_page = args.pop('per_page')

        query = apply_filter_map(Author.query, args, filter_map)
        query = query.paginate(page=page, per_page=per_page, error_out=False)

        return PaginatedAuthorWithBooksSchema().dump(query), HTTPStatus.OK


class AuthorItem(Resource):
    @api.response(200, "OK", get_swagger_model(api, AuthorWithBooksSchema))
    def get(self, id, **kwargs):
        author = Author.query.get(id)
        return AuthorWithBooksSchema().dump(author), HTTPStatus.OK
