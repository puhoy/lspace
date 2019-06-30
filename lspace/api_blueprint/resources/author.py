from lspace.api_blueprint import api
from lspace.api_blueprint.models import author_with_books_model
from lspace.api_blueprint.sqlalchemy_resource import SqlAlchemyResource
from lspace.models import Author, Book

author_filters = ['name']

filter_map = {
    'books': lambda value: Author.books.any(Book.title.ilike(value)),
    '__default': lambda key, value: getattr(Author, key).ilike(value)
}

alchemy_author = SqlAlchemyResource(api_object=api,
                                  model=Author,
                                  marshal_with=author_with_books_model,
                                  filters=author_filters,
                                  filter_map=filter_map)
