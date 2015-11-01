__author__ = 'alan'
from flask import Flask, request

PORT = 9103


def get_app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        print request.host
        print request.url
        return str(PORT)

    return app


if __name__ == "__main__":
    get_app().run(port=PORT)