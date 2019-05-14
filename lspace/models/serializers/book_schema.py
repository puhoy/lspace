from lspace.app import marshmallow
from lspace.models import Book
from lspace.models.serializers.author_schema import AuthorSchema


class BookSchema(marshmallow.ModelSchema):
    authors = marshmallow.Nested(AuthorSchema, many=True)

    class Meta:
        model = Book
        #fields = ('id', 'author')
