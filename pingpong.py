from flask_restful import Resource


# class for healthcheck service
class PingPong(Resource):

    def get(self):
        return 'pong'
