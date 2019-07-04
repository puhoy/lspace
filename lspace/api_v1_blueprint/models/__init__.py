from flask import url_for
from marshmallow import Schema, fields, post_load

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
    id = fields.Int()
    title = fields.String()
    authors = fields.Nested(AuthorSchema, many=True)
    shelf = fields.Nested(ShelfSchema, allow_none=True)
    isbn13 = fields.String(default=None, allow_none=True)
    md5sum = fields.String()
    publisher = fields.String()
    metadata_source = fields.String()
    year = fields.Integer()
    language = fields.String()
    url = fields.Method(serialize='get_url',
                        deserialize='load_url')

    def get_url(self, book):
        return url_for('api.book_file', md5sum=book.md5sum)

    def load_url(self, value):
        return value

    # 'file': fields.String(attribute=lambda book: url_for('api.book_file', md5sum=book.md5sum))

    @post_load
    def make_book(self, data, **kwargs):
        print('making book!')
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
        book.url = data['url']
        return book


class ShelfWithBooksSchema(ShelfSchema):
    books = fields.Nested(BookSchema, many=True)


class AuthorWithBooksSchema(AuthorSchema):
    books = fields.Nested(BookSchema, many=True)
