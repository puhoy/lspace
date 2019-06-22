from flask import Blueprint
from flask_restplus import Api

api_blueprint = Blueprint('api', __name__,
                        template_folder='templates')

api = Api(api_blueprint, version='1.0', title='L-Space API',
    description='L-Space API',
)

@api_blueprint.after_request
def add_gnu_tp_header(response):
    # www.gnuterrypratchett.com
    response.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
    return response

from lspace.api_blueprint.apis.version import Version
from lspace.api_blueprint.apis.book import BookItem, BookCollection
from lspace.api_blueprint.apis.author import AuthorItem, AuthorCollection
