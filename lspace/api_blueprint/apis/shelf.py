
from lspace.api_blueprint import api
from lspace.api_blueprint.models import shelf_with_books_model
from lspace.api_blueprint.sqlalchemy_resource import SqlAlchemyResource
from lspace.models import Shelf



shelf_filters = ['name']

filter_map = {
    '__default': lambda key, value: getattr(Shelf, key).ilike(value)
}

alchemy_shelf = SqlAlchemyResource(api_object=api,
                                  model=Shelf,
                                  marshal_with=shelf_with_books_model,
                                  filters=shelf_filters,
                                  filter_map=filter_map)

