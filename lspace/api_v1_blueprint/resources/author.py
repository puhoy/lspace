from lspace.api_v1_blueprint import api
from lspace.api_v1_blueprint.models import AuthorWithBooksSchema
from lspace.api_v1_blueprint.sqlalchemy_resource import SqlAlchemyResource
from lspace.models import Author, Book

author_filters = ['name']

filter_map = {
    'books': lambda value: Author.books.any(Book.title.ilike(value)),
    '__default': lambda key, value: getattr(Author, key).ilike(value)
}

alchemy_author = SqlAlchemyResource(api_object=api,
                                  model=Author,
                                  marshmallow_schema=AuthorWithBooksSchema,
                                  filters=author_filters,
                                  filter_map=filter_map)
