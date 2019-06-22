from flask_restplus import fields, reqparse

from lspace.api_blueprint import api

shelve_model = api.model('Shelve', {
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
    'shelve': fields.Nested(shelve_model),
    'isbn13': fields.String
})

author_with_books_model = api.inherit('AuthorWithBooks', author_model, {
    'books': fields.List(fields.Nested(book_model))
})


def get_paginated_model(model):
    paginate_model = api.model('Page', {
        'prev_num': fields.Integer,
        'next_num': fields.Integer,
        'has_next': fields.Boolean,
        'has_prev': fields.Boolean,
        'items': fields.Nested(model)
    })
    return paginate_model



pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False)
pagination_arguments.add_argument('per_page', type=int, required=False, default=50)
