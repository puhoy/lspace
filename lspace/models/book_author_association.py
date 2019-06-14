from lspace import db

book_author_association_table = db.Table('book_author_association',
                                         db.Column('book_id',
                                                   db.Integer,
                                                   db.ForeignKey('books.id'),
                                                   ),
                                         db.Column('author_id',
                                                   db.Integer,
                                                   db.ForeignKey('authors.id'))
                                         )
