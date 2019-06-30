from flask_restplus import Resource

class Version(Resource):

    def get(self, **kwargs):
        from lspace import __version__, APP_NAME
        return dict(version='{APP_NAME}-{VERSION}'.format(VERSION=__version__, APP_NAME=APP_NAME))
