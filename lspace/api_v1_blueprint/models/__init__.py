from marshmallow import Schema, fields, post_load

from lspace.models import Author, Shelf, Book


class ShelfSchema(Schema):
    id = fields.Int()
    name = fields.String()

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
    shelf = fields.Nested(ShelfSchema)
    isbn13 = fields.String()
    md5sum = fields.String()
    publisher = fields.String()
    metadata_source = fields.String()
    year = fields.Integer()
    language = fields.String()
    file = fields.Url()

    @post_load
    def make_book(self, data, **kwargs):
        book = Book()
        book.title = self.title
        book.authors = self.authors
        book.shelf = self.shelf
        book.isbn13 = self.isbn13
        book.md5sum = self.md5sum
        book.publisher = self.publisher
        book.metadata_source = self.metadata_source
        book.year = self.year
        book.language = self.language
        book.file = self.file
        return book


class ShelfWithBooksSchema(ShelfSchema):
    books = fields.Nested(BookSchema, many=True)

class AuthorWithBooksSchema(AuthorSchema):
    books = fields.Nested(BookSchema, many=True)

