from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint('api', __name__,
                          template_folder='templates')

api = Api(api_blueprint, version='1.0', title='L-Space API',
          description='L-Space API',
          )

from lspace.api_v1_blueprint.resources.book import BookItem, BookCollection
from lspace.api_v1_blueprint.resources.book_file import BookFile

from lspace.api_v1_blueprint.resources.version import Version

api.add_resource(BookItem, '/books/<int:id>')
api.add_resource(BookCollection, '/books/')

api.add_resource(BookFile, '/files/books/<md5sum>')
# api.add_resource('', '/files/covers/<md5>')

api.add_resource(Version, '/version/')
