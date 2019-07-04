from urllib.parse import urlparse, ParseResult
import requests

# from lspace.api_v1_blueprint.models import author_with_books_model, shelf_with_books_model, book_model
from lspace.api_v1_blueprint.models import BookSchema, AuthorWithBooksSchema, ShelfWithBooksSchema
from lspace.api_v1_blueprint.sqlalchemy_resource import SqlAlchemyResource, get_paginated_marshmallow_schema

detail_path_serializer_map = {
    'books/': get_paginated_marshmallow_schema(BookSchema),
    'books/1': BookSchema,
    'authors/': get_paginated_marshmallow_schema(AuthorWithBooksSchema),
    'shelves/': get_paginated_marshmallow_schema(ShelfWithBooksSchema)
}


class ApiImporter:
    def __init__(self, url):
        self.url = url
        parsed = urlparse(url)
        path = parsed.path

        clean_api_base_path = '/api/v1/'
        splits = path.rpartition(clean_api_base_path)

        self.detail_path = splits[2]

        self.session = requests.session()

    def import_books(self):
        print(self.detail_path)

        serializer: BookSchema = detail_path_serializer_map[self.detail_path]()

        response = self.session.get(self.url)
        print(response.json())
        book_list = serializer.load(response.json()).data
        print(book_list['items'])

        # print(marshal(response.json().get('resource'), book_model))

        exit(1)

        # if not skip_library_check and Book.query.filter_by(md5sum=file_type_object.get_md5()).first():
