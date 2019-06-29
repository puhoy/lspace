from flask_restplus import Resource, reqparse, fields
from flask_sqlalchemy import Pagination


def get_pagination_arguments():
    pagination_arguments = reqparse.RequestParser()
    pagination_arguments.add_argument('page', type=int, required=False)
    pagination_arguments.add_argument('per_page', type=int, required=False, default=50)
    pagination_arguments.add_argument('max_per_page', type=int, required=False, default=50)
    return pagination_arguments


def get_filters(*fields):
    filter_fields = reqparse.RequestParser()
    for field in fields:
        filter_fields.add_argument(field, type=str, required=False, store_missing=False)
    return filter_fields


class SqlAlchemyResource:

    def __init__(self, api_object, model, marshal_with, filters, filter_map):
        self.api_object = api_object
        self.model = model
        self.marshal_with = marshal_with
        self.filters = get_filters(*filters)
        self.filter_map = filter_map

        self.paginated_model = api_object.model('Page', {
            'prev_num': fields.Integer,
            'next_num': fields.Integer,
            'has_next': fields.Boolean,
            'has_prev': fields.Boolean,
            'items': fields.Nested(self.marshal_with)
        })

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
        resource_marshal_with = self.marshal_with
        resource_model = self.model
        resource_api_object = self.api_object

        class Item(Resource):
            @resource_api_object.marshal_with(resource_marshal_with, envelope='resource')
            def get(self, id, **kwargs):
                return resource_model.query.get(id)

        return Item

    def get_collection(self):
        resource_api_object = self.api_object
        resource_filters = self.filters
        resource_model = self.model
        resource_filter_map = self.filter_map

        resource_paginated_model = self.paginated_model

        class Collection(Resource):
            @resource_api_object.expect(resource_filters, validate=True)
            @resource_api_object.expect(get_pagination_arguments(), validate=True)
            @resource_api_object.marshal_with(resource_paginated_model)
            def get(self, **kwargs):
                args = get_pagination_arguments().parse_args()
                filter_args = resource_filters.parse_args()
                q = SqlAlchemyResource.apply_filter_map(resource_model.query, filter_args, resource_filter_map)
                q: Pagination = q.paginate(page=args['page'], per_page=args['per_page'], max_per_page=args['max_per_page'],
                           error_out=False)
                return q

        return Collection
