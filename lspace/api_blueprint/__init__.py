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


from lspace.api_blueprint.resources.book import alchemy_book
from lspace.api_blueprint.resources.author import alchemy_author
from lspace.api_blueprint.resources.shelf import alchemy_shelf
from lspace.api_blueprint.resources.book_file import BookFile

from lspace.api_blueprint.resources.version import Version

api.add_resource(alchemy_book.get_item(), '/books/<int:id>')
api.add_resource(alchemy_book.get_collection(), '/books/')

api.add_resource(alchemy_author.get_item(), '/authors/<int:id>')
api.add_resource(alchemy_author.get_collection(), '/authors/')

api.add_resource(alchemy_shelf.get_item(), '/shelves/<int:id>')
api.add_resource(alchemy_shelf.get_collection(), '/shelves/')

api.add_resource(BookFile, '/files/books/<md5sum>')
#api.add_resource('', '/files/covers/<md5>')

api.add_resource(Version, '/version/')