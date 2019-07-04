from urllib.parse import urlparse

import click
import requests

from lspace.api_v1_blueprint.models import BookSchema, AuthorWithBooksSchema, ShelfWithBooksSchema
from lspace.api_v1_blueprint.sqlalchemy_resource import get_paginated_marshmallow_schema
from lspace.models import Book

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

    def import_books(self, skip_library_check):
        print(self.detail_path)

        serializer = detail_path_serializer_map[self.detail_path]()

        response = self.session.get(self.url)
        print(response.json())

        book_list = serializer.load(response.json())['items']

        print(book_list)

        for book in book_list:
            if not skip_library_check and Book.query.filter_by(md5sum=book.md5sum).first():
                click.echo(click.secho('already imported, skipping...', bold=True))
                continue

            print(book.url)
        exit(1)

        print(book_list['items'])

        # print(marshal(response.json().get('resource'), book_model))

        exit(1)
