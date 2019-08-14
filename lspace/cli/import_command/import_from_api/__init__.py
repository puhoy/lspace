import logging
import os
import re
import tempfile
from urllib.parse import urlparse, parse_qs, urlsplit, urlunsplit, urlencode

import requests
from flask import current_app
from typing import List

from lspace.api_v1_blueprint.models import BookSchema, PaginatedBookSchema
from lspace.cli.import_command.copy_to_library import find_unused_path
from lspace.models import Book

logger = logging.getLogger(__name__)


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

        self.detail_path_import_function_map = {
            '^(?:books\/)$': self.fetch_from_books_route,
            '^(?:books\/)([0-9]+)$': self.fetch_from_book_route
        }

    def fetch_from_books_route(self):
        next_url = self.url
        while next_url:
            paginated_response = session.get(next_url).json()
            paginated_books = PaginatedBookSchema().load(paginated_response)

            books = paginated_books['items']
            yield from self.get_books(books)
            next_url = _get_next_page_url(next_url, paginated_response)

    def fetch_from_book_route(self):
        book_response = session.get(self.url).json()
        book = BookSchema().load(book_response)
        return self.get_books([book])

    def get_book(self, tmpdirname, book):
        temp_path = find_unused_path(tmpdirname, current_app.config['USER_CONFIG']['file_format'], book)
        abs_temp_path = os.path.join(tmpdirname, temp_path)
        if not os.path.isdir(os.path.dirname(abs_temp_path)):
            os.makedirs(os.path.dirname(abs_temp_path))
        book_url = urlunsplit((self.scheme, self.netloc, book.url, '', ''))
        download_file(book_url, abs_temp_path)
        return abs_temp_path, book

    def get_books(self, books):
        # type: (List[Book]) -> (str, Book)
        with tempfile.TemporaryDirectory() as tmpdirname:
            for book in books:
                yield self.get_book(tmpdirname, book)

    def start_import(self, skip_library_check):
        for route_regex, function in self.detail_path_import_function_map.items():
            if re.match(route_regex, self.detail_path):
                yield from function()
                return
