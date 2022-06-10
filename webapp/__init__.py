
from flask import Flask
from webapp.model import db


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    
    @app.route('/')
    def trails():
        return'test'

    return app