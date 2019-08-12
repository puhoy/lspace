from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_restplus import reqparse
from marshmallow import Schema, fields


def get_pagination_args_parser():
    pagination_arguments = reqparse.RequestParser()
    pagination_arguments.add_argument('page', type=int, required=False)
    pagination_arguments.add_argument('per_page', type=int, required=False, default=50)
    return pagination_arguments


def add_fields_to_parser(parser, fields):
    for field in fields:
        parser.add_argument(field, type=str, required=False, store_missing=False)
    return parser


def get_paginated_marshmallow_schema(marshmallow_schema):
    class Paginated(Schema):
        prev_num = fields.Integer(allow_none=True)
        next_num = fields.Integer(allow_none=True)
        has_next = fields.Boolean()
        has_prev = fields.Boolean()
        total = fields.Integer()
        page = fields.Integer()
        items = fields.Nested(marshmallow_schema, many=True)

    Paginated.__name__ = 'Paginated' + marshmallow_schema.__name__
    return Paginated


def apply_filter_map(query, filter_args, filter_map):
    filters = []
    for key, value in filter_args.items():
        if key in filter_map.keys():
            filters.append(filter_map[key](value))
        else:
            filters.append(filter_map['__default'](key, value))
    return query.filter(*filters)


def get_swagger_model(api_object, marshmallow_schema):
    # https://github.com/noirbizarre/flask-restplus/issues/438#issuecomment-490951796
    spec = APISpec(
        title=api_object.title,
        version=api_object.version,
        openapi_version="2.0",
        plugins=[MarshmallowPlugin(schema_name_resolver=lambda _: None)],
        info=dict(description=api_object.description)
    )
    schema2jsonschema = spec.plugins.pop().openapi.schema2jsonschema

    json_schema = schema2jsonschema(schema=marshmallow_schema)

    swagger_schema_model = api_object.schema_model(marshmallow_schema.__name__, json_schema)
    return swagger_schema_model


def run_query(Model, args, filter_map, page, per_page):
    query = apply_filter_map(Model.query, args, filter_map)
    query = query.paginate(page=page, per_page=per_page, error_out=False)
    return query
