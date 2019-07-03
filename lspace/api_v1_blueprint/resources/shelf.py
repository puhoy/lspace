
from lspace.api_v1_blueprint import api
from lspace.api_v1_blueprint.models import ShelfWithBooksSchema
from lspace.api_v1_blueprint.sqlalchemy_resource import SqlAlchemyResource
from lspace.models import Shelf



shelf_filters = ['name']

filter_map = {
    '__default': lambda key, value: getattr(Shelf, key).ilike(value)
}

alchemy_shelf = SqlAlchemyResource(api_object=api,
                                  model=Shelf,
                                  marshmallow_schema=ShelfWithBooksSchema,
                                  filters=shelf_filters,
                                  filter_map=filter_map)

