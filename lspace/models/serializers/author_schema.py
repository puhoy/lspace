from lspace import marshmallow
from lspace.models import Author


class AuthorSchema(marshmallow.ModelSchema):
    class Meta:
        model = Author
        fields = ('name',)
