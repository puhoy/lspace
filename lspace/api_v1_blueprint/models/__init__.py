from flask import url_for
from marshmallow import Schema, fields, post_load, EXCLUDE

from lspace.api_v1_blueprint.resource_helpers import get_paginated_marshmallow_schema
from lspace.models import Author, Shelf, Book


class ShelfSchema(Schema):
    id = fields.Int()
    name = fields.String(required=False)

    @post_load
    def make_shelf(self, data, **kwargs):
        shelf = Shelf.query.filter_by(name=data['name']).first()
        if not shelf:
            shelf = Shelf()
            shelf.name = data['name']
        return shelf


class AuthorSchema(Schema):
    id = fields.Int()
    name = fields.String()

    @post_load
    def make_author(self, data, **kwargs):
        author = Author.query.filter_by(name=data['name']).first()
        if not author:
            author = Author()
            author.name = data['name']
        return author


class BookSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True, missing=None)
    title = fields.String()
    authors = fields.Nested(AuthorSchema, many=True)
    shelf = fields.Nested(ShelfSchema, allow_none=True)
    isbn13 = fields.String(default=None, allow_none=True)
    md5sum = fields.String()
    publisher = fields.String(allow_none=True)
    metadata_source = fields.String(allow_none=True)
    year = fields.Integer(allow_none=True)
    language = fields.String(allow_none=True)
    path = fields.String()
    url = fields.Method(serialize='get_url',
                        deserialize='load_url')

    def get_url(self, book):
        return url_for('api.book_file', md5sum=book.md5sum)

    def load_url(self, value):
        return value

    @post_load
    def make_book(self, data, **kwargs):
        book = Book.query.filter_by(md5sum=data['md5sum']).first()
        if not book:
            book = Book()
            book.title = data['title']
            book.authors = data['authors']
            book.shelf = data['shelf']
            book.isbn13 = data['isbn13']
            book.md5sum = data['md5sum']
            book.publisher = data['publisher']
            book.metadata_source = data['metadata_source']
            book.year = data['year']
            book.language = data['language']

        book.path = data['path']
        book.url = data['url']
        return book


PaginatedBookSchema = get_paginated_marshmallow_schema(BookSchema)
