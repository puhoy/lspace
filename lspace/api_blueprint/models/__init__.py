from flask_restplus import fields, reqparse

from lspace.api_blueprint import api

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
    'isbn13': fields.String
})

author_with_books_model = api.inherit('AuthorWithBooks', author_model, {
    'books': fields.List(fields.Nested(book_model))
})

