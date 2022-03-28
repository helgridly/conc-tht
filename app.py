import flask
from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

routes = flask.Blueprint('tube-service', __name__)
api = Api(routes, version='0.1', title='Tubes Service',
          description='tubes service')

ns = api.namespace('/', description='tube handling')
app.register_blueprint(routes)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)


class Tube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.String, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey(Patient.id), nullable=False)


@ns.route("/tubes")
class Tubes(Resource):
    def get(self):
        return {"hello": "world"}
