from flask_restplus import Resource
from flask_restplus._http import HTTPStatus

from lspace.api_v1_blueprint import api
from lspace.api_v1_blueprint.models import BookSchema, PaginatedBookSchema
from lspace.api_v1_blueprint.resource_helpers import get_pagination_args_parser, \
    add_fields_to_parser, \
    apply_filter_map, get_swagger_model
from lspace.models import Book, Shelf, Author

filter_fields = ['title', 'publisher', 'shelf', 'author', 'md5sum', 'language']


args_parser = get_pagination_args_parser()
add_fields_to_parser(args_parser, filter_fields)


filter_map = {
    'shelf': lambda value: Book.shelf.has(Shelf.name.ilike(value)),
    'author': lambda value: Book.authors.any(Author.name.ilike(value)),

    '__default': lambda key, value: getattr(Book, key).ilike(value)
}


paginated_schemamodel = get_swagger_model(api, PaginatedBookSchema)
schemamodel = get_swagger_model(api, BookSchema)

class BookCollection(Resource):

    @api.expect(args_parser, validate=True)
    @api.response(200, "OK", paginated_schemamodel)
    def get(self):
        args = args_parser.parse_args()
        page = args.pop('page')
        per_page = args.pop('per_page')
        query = apply_filter_map(Book.query, args, filter_map)

        query = query.paginate(page=page, per_page=per_page, error_out=False)

        return PaginatedBookSchema().dump(query), HTTPStatus.OK


class BookItem(Resource):
    @api.response(200, "OK", schemamodel)
    def get(self, id, **kwargs):
        book = Book.query.get(id)
        return BookSchema().dump(book), HTTPStatus.OK
