
from urllib.parse import urlparse, ParseResult
import requests




#from lspace.api_v1_blueprint.models import author_with_books_model, shelf_with_books_model, book_model

detail_path_serializer_map = {
#    'books/': book_model,
    'books/<id>': '',
    'authors/': '',
    'shelves/': ''
}


class ApiImporter:
    def __init__(self, url):
        self.url = url
        parsed: ParseResult = urlparse(url)
        path = parsed.path

        clean_api_base_path = '/api/v1/'
        splits = path.rpartition(clean_api_base_path)

        self.detail_path = splits[2]

        self.session = requests.session()

    def import_books(self):
        print(self.detail_path)

        response = self.session.get(self.url)
        print(response.json().get('resource'))
        print(marshal(response.json().get('resource'), book_model))


        exit(1)



        #if not skip_library_check and Book.query.filter_by(md5sum=file_type_object.get_md5()).first():



