from flask_restx import Resource

from flask import send_file
from lspace.models import Book

import logging

logger = logging.getLogger(__name__)


class BookFile(Resource):

    def get(self, md5sum, **kwargs):
        book = Book.query.filter_by(md5sum=md5sum).first()
        attachment_filename = '{authors_slug}-{title_slug}{extension}'.format(
            authors_slug=book.author_names_slug,
            title_slug=book.title_slug,
            extension=book.extension
        )
        logger.debug(f"sending {book.full_path}")
        return send_file(book.full_path,
                         as_attachment=True,
                         attachment_filename=attachment_filename)
