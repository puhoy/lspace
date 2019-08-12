from flask_restplus import Resource
from flask_restplus._http import HTTPStatus

from lspace.api_v1_blueprint import api
from lspace.api_v1_blueprint.models import ShelfSchema, PaginatedShelfWithBooksSchema
from lspace.api_v1_blueprint.resource_helpers import get_pagination_args_parser, \
    add_fields_to_parser, \
    get_swagger_model, run_query
from lspace.models import Shelf

filter_fields = ['name']

args_parser = get_pagination_args_parser()
add_fields_to_parser(args_parser, filter_fields)

filter_map = {
    '__default': lambda key, value: getattr(Shelf, key).ilike(value)
}


class ShelfCollection(Resource):
    @api.expect(args_parser, validate=True)
    @api.response(200, "OK", get_swagger_model(api, PaginatedShelfWithBooksSchema))
    def get(self):
        args = args_parser.parse_args()
        page = args.pop('page')
        per_page = args.pop('per_page')
        query = run_query(Shelf, args, filter_map, page, per_page)

        return PaginatedShelfWithBooksSchema().dump(query), HTTPStatus.OK


class ShelfItem(Resource):
    @api.response(200, "OK", get_swagger_model(api, ShelfSchema))
    def get(self, id, **kwargs):
        shelf = Shelf.query.get(id)
        return ShelfSchema().dump(shelf), HTTPStatus.OK
