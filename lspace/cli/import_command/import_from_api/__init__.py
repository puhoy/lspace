import os
import tempfile
from urllib.parse import urlparse, parse_qs, urlsplit, urlunsplit, urlencode

import requests
from flask import current_app

from lspace.api_v1_blueprint.models import BookSchema, AuthorWithBooksSchema, ShelfWithBooksSchema
from lspace.api_v1_blueprint.sqlalchemy_resource import get_paginated_marshmallow_schema
from lspace.cli.import_command.copy_to_library import find_unused_path

PaginatedBookSchema = get_paginated_marshmallow_schema(BookSchema)
PaginatedAuthorWithBooksSchema = get_paginated_marshmallow_schema(AuthorWithBooksSchema)
PaginatedShelfWithBooksSchema = get_paginated_marshmallow_schema(ShelfWithBooksSchema)


def _get_next_page_url(url, response):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    next_num = response.get('next_num')

    if next_num:
        query_params['page'] = [next_num]
    else:
        return False

    query_string = urlencode(query_params, doseq=True)
    return urlunsplit((scheme, netloc, path, query_string, fragment))


def download_file(url, destination_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(destination_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return True


def get_book(url):
    pass


def get_authors(url):
    pass


def get_author(url):
    pass


def get_shelve(url):
    pass


def get_shelves(url):
    pass


session = requests.session()


class ApiImporter:
    def __init__(self, url):
        self.url = url
        parsed = urlparse(url)
        self.scheme = parsed.scheme
        self.netloc = parsed.netloc
        self.path = parsed.path
        self.fragment = parsed.fragment

        path = parsed.path

        clean_api_base_path = '/api/v1/'
        splits = path.rpartition(clean_api_base_path)

        self.detail_path = splits[2]

        self.detail_path_imprt_function_map = {
            '^(?:books\/)$': self.get_books,
            '^(?:books\/)([0-9]+)$': get_book,
            'authors/': get_authors,
            '^(?:authors\/)([0-9]+)$': get_author,
            'shelves/': get_shelves,
            '^(?:shelves\/)([0-9]+)$': get_shelve,
        }

    def fetch_from_books_route(self):
        
        next_url = self.url
        while next_url:
        
            paginated_response = session.get(next_url).json()
            paginated_books = PaginatedBookSchema().load(paginated_response)

            books = paginated_books['items']

            yield from self.get_books(books)

            next_url = _get_next_page_url(next_url, paginated_response)

            print(next_url)

    def get_books(self, books):
        # type: (List(Book)) -> (str, Book)

        with tempfile.TemporaryDirectory() as tmpdirname:
            for book in books:

                temp_path = find_unused_path(tmpdirname, current_app.config['USER_CONFIG']['file_format'], book)
                abs_temp_path = os.path.join(tmpdirname, temp_path)
                if not os.path.isdir(os.path.dirname(abs_temp_path)):
                    os.makedirs(os.path.dirname(abs_temp_path))

                book_url = urlunsplit((self.scheme, self.netloc, book.url, '', ''))
                download_file(book_url, abs_temp_path)
                yield abs_temp_path, book

    def import_books(self, skip_library_check):
        return self.fetch_from_books_route()
