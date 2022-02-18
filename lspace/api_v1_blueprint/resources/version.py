from flask_restx import Resource


class Version(Resource):

    def get(self, **kwargs):
        from lspace import __version__, APP_NAME
        return dict(name=APP_NAME, version=__version__)
