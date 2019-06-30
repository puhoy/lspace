from flask import url_for
from flask_restplus import fields

from lspace.api_blueprint import api
from lspace.api_blueprint.resources.book_file import BookFile

shelf_model = api.model('Shelf', {
    'id': fields.Integer,
    'name': fields.String,
})

author_model = api.model('Author', {
    'id': fields.Integer,
    'name': fields.String,
})

book_model = api.model('Book', {
    'id': fields.Integer,
    'title': fields.String,
    'authors': fields.List(fields.Nested(author_model)),
    'shelf': fields.Nested(shelf_model),
    'isbn13': fields.String,
    'md5sum': fields.String,
    'file': fields.String(attribute=lambda book: url_for('api.book_file', md5sum=book.md5sum))
})

author_with_books_model = api.inherit('AuthorWithBooks', author_model, {
    'books': fields.List(fields.Nested(book_model))
})

shelf_with_books_model = api.inherit('ShelfWithBooks', author_model, {
    'books': fields.List(fields.Nested(book_model))
})
