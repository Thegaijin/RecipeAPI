from flask_restplus import Namespace, Resource

api = Namespace('hello', description='Hello world')


@api.route('/')
class Hello(Resource):
    def get(self):
        ''' Method returns a phrase '''

        return {'Welcome': 'Hello world'}
