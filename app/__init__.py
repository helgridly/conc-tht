import flask

from app.app import routes
from app.db import db

def create_app():
    app = flask.Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
    app.config["RESTX_MASK_SWAGGER"] = False  # disable X-Fields header in swagger
    app.register_blueprint(routes)
    db.init_app(app)
    return app
