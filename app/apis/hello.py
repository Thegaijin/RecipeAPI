# /app/apis/hello.py
''' This script returns a string '''

# Third-party imoport
from flask_restplus import Namespace, Resource

api = Namespace('hello', description='Hello world')


@api.route('/')
class Hello(Resource):
    def get(self):
        ''' Method returns a phrase '''

        return {'Welcome': 'Hello world'}
