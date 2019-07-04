from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_restplus import Resource, reqparse
from flask_restplus._http import HTTPStatus
from marshmallow import Schema, fields, post_load


def get_pagination_arguments():
    pagination_arguments = reqparse.RequestParser()
    pagination_arguments.add_argument('page', type=int, required=False)
    pagination_arguments.add_argument('per_page', type=int, required=False, default=50)
    return pagination_arguments


def get_filters(*fields):
    filter_fields = reqparse.RequestParser()
    for field in fields:
        filter_fields.add_argument(field, type=str, required=False, store_missing=False)
    return filter_fields


def get_paginated_marshmallow_schema(marshmallow_schema):
    class Paginated(Schema):
        prev_num = fields.Integer(allow_none=True)
        next_num = fields.Integer(allow_none=True)
        has_next = fields.Boolean()
        has_prev = fields.Boolean()
        items = fields.Nested(marshmallow_schema, many=True)

    Paginated.__name__ = 'Paginated' + marshmallow_schema.__name__
    return Paginated


# https://github.com/noirbizarre/flask-restplus/issues/438#issuecomment-490951796
def resolver(schema):
    return None


class SqlAlchemyResource:

    def __init__(self, api_object, model, marshmallow_schema, filters, filter_map):
        self.api_object = api_object
        self.alchemy_model = model
        self.marshmallow_schema = marshmallow_schema
        self.paginated_marshmallow_schema = get_paginated_marshmallow_schema(marshmallow_schema)
        self.filters = get_filters(*filters)
        self.filter_map = filter_map

        self._setup_swagger()

    def _setup_swagger(self):
        self.spec = APISpec(
            title=self.api_object.title,
            version=self.api_object.version,
            openapi_version="2.0",
            plugins=[MarshmallowPlugin(schema_name_resolver=resolver)],
            info=dict(description=self.api_object.description)
        )
        schema2jsonschema = self.spec.plugins.pop().openapi.schema2jsonschema

        json_schema = schema2jsonschema(schema=self.marshmallow_schema)
        paginated_json_schema = schema2jsonschema(schema=self.paginated_marshmallow_schema)

        self.swagger_schema_model = self.api_object.schema_model(self.marshmallow_schema.__name__, json_schema)
        self.swagger_paginated_schema_model = \
            self.api_object.schema_model(self.paginated_marshmallow_schema.__name__, paginated_json_schema)

    @classmethod
    def apply_filter_map(cls, query, filter_args, filter_map):
        filters = []
        for key, value in filter_args.items():
            if key in filter_map.keys():
                filters.append(filter_map[key](value))
            else:
                filters.append(filter_map['__default'](key, value))
        return query.filter(*filters)

    def get_item(self):
        wrapper_self = self

        class Item(Resource):
            @wrapper_self.api_object.response(200, "OK", wrapper_self.swagger_schema_model)
            def get(self, id, **kwargs):
                return wrapper_self.marshmallow_schema().dump(
                    wrapper_self.alchemy_model.query.get(id)), HTTPStatus.OK

        return Item

    def get_collection(self):
        wrapper_self = self

        class Collection(Resource):

            @wrapper_self.api_object.expect(wrapper_self.filters, validate=True)
            @wrapper_self.api_object.expect(get_pagination_arguments(), validate=True)
            @wrapper_self.api_object.response(200, "OK", wrapper_self.swagger_paginated_schema_model)
            def get(self, **kwargs):
                args = get_pagination_arguments().parse_args()
                filter_args = wrapper_self.filters.parse_args()
                q = SqlAlchemyResource.apply_filter_map(wrapper_self.alchemy_model.query, filter_args,
                                                        wrapper_self.filter_map)
                q = q.paginate(page=args['page'], per_page=args['per_page'], error_out=False)

                return wrapper_self.paginated_marshmallow_schema().dump(q), HTTPStatus.OK

        return Collection
