from apispec import APISpec
from flask_restplus import Resource, reqparse
from flask_restplus._http import HTTPStatus
from flask_sqlalchemy import Pagination
from marshmallow import Schema, fields


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


# https://github.com/noirbizarre/flask-restplus/issues/438#issuecomment-490951796
from apispec.ext.marshmallow import MarshmallowPlugin


def resolver(schema):
    return None


class SqlAlchemyResource:

    def __init__(self, api_object, model, marshmallow_schema, filters, filter_map):
        self.api_object = api_object
        self.model = model
        self.marshmallow_schema = marshmallow_schema
        self.filters = get_filters(*filters)
        self.filter_map = filter_map

        self.spec = APISpec(
            title=self.api_object.title,
            version=self.api_object.version,
            openapi_version="2.0",
            plugins=[MarshmallowPlugin(schema_name_resolver=resolver)],
            info=dict(description=self.api_object.description)
        )
        schema2jsonschema = self.spec.plugins.pop().openapi.schema2jsonschema

        json_schema = schema2jsonschema(schema=self.marshmallow_schema)
        paginated_json_schema = schema2jsonschema(schema=self.get_paginated_marshmallow_schema())
        self.schema_model = self.api_object.schema_model(self.marshmallow_schema.__name__, json_schema)
        self.paginated_schema_model = self.api_object.schema_model(self.get_paginated_marshmallow_schema().__name__, paginated_json_schema)

    def get_paginated_marshmallow_schema(self):
        class Paginated(Schema):
            prev_num = fields.Integer()
            next_num = fields.Integer()
            has_next = fields.Boolean()
            has_prev = fields.Boolean()
            items = fields.Nested(self.marshmallow_schema, many=True)
        Paginated.__name__ = self.marshmallow_schema.__name__ + 'Paginated'
        return Paginated

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
        resource_marshmallow_schema = self.marshmallow_schema
        resource_model = self.model
        resource_schema_model = self.schema_model
        resource_api_object = self.api_object

        class Item(Resource):
            @resource_api_object.response(200, "OK", resource_schema_model)
            def get(self, id, **kwargs):
                return resource_marshmallow_schema().dump(resource_model.query.get(id)).data, HTTPStatus.OK

        return Item

    def get_collection(self):
        resource_api_object = self.api_object
        resource_filters = self.filters
        resource_model = self.model
        resource_filter_map = self.filter_map
        resource_paginated_json_schema = self.paginated_schema_model

        resource_paginated_schema = self.get_paginated_marshmallow_schema()

        class Collection(Resource):


            @resource_api_object.expect(resource_filters, validate=True)
            @resource_api_object.expect(get_pagination_arguments(), validate=True)
            @resource_api_object.response(200, "OK", resource_paginated_json_schema)
            def get(self, **kwargs):
                args = get_pagination_arguments().parse_args()
                filter_args = resource_filters.parse_args()
                q = SqlAlchemyResource.apply_filter_map(resource_model.query, filter_args, resource_filter_map)
                q: Pagination = q.paginate(page=args['page'], per_page=args['per_page'], error_out=False)
                print(resource_paginated_schema().dump(q).data)
                return resource_paginated_schema().dump(q).data, HTTPStatus.OK

        return Collection
