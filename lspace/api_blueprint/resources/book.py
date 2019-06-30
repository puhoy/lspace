from lspace.api_blueprint import api
from lspace.api_blueprint.models import book_model
from lspace.api_blueprint.sqlalchemy_resource import SqlAlchemyResource
from lspace.models import Book, Shelf, Author



book_filters = ['title', 'publisher', 'shelf', 'author', 'md5sum', 'language']

filter_map = {
    'shelf': lambda value: Book.shelf.has(Shelf.name.ilike(value)),
    'author': lambda value: Book.authors.any(Author.name.ilike(value)),

    '__default': lambda key, value: getattr(Book, key).ilike(value)
}

alchemy_book = SqlAlchemyResource(api_object=api,
                                  model=Book,
                                  marshal_with=book_model,
                                  filters=book_filters,
                                  filter_map=filter_map)

