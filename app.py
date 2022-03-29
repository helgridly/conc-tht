import flask
from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

import uuid
import enum

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config["RESTX_MASK_SWAGGER"] = False  # disable X-Fields header in swagger
db = SQLAlchemy(app)

routes = flask.Blueprint('tube-service', __name__)
api = Api(routes, version='0.1', title='Tubes Service',
          description='tubes service')

ns = api.namespace('/', description='tube handling')
app.register_blueprint(routes)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)

    @classmethod
    def get_or_create(cls, email: str):
        inst = db.session.query(Patient).filter(Patient.email == email).first()
        if not inst:
            inst = Patient()
            inst.email = email
            db.session.add(inst)
            db.session.commit()
        return inst

@enum.unique
class TubeStatus(enum.Enum):
    registered = 10
    received = 20
    positive = 30
    negative = 40
    indeterminate = 50

    def __str__(self):
        return self.name

    @classmethod
    def from_string(cls, name: str):
        try:
            return TubeStatus[name]
        except KeyError:
            raise NotImplementedError(f"Unknown TubeStatus enum {name}")

class Tube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.Enum(TubeStatus), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey(Patient.id), nullable=False)

    @classmethod
    def get_model(cls):
        return {
            "barcode": fields.String,
            "status": fields.String
        }

tube_info = ns.model("TubeInfo", Tube.get_model())


@ns.route("/tubes")
class Tubes(Resource):
    @ns.marshal_list_with(tube_info)
    def get(self):
        tubes = db.session.query(Tube).filter(Tube.status == 'registered').all()
        return tubes

    @ns.expect(api.model('NewTube', {'patient_email': fields.String}), validate=True)
    @ns.marshal_with(tube_info)
    def post(self):
        new_tube = Tube()
        new_tube.barcode = str(uuid.uuid4())
        new_tube.status = "registered"
        new_tube.patient_id = Patient.get_or_create(api.payload['patient_email']).id
        db.session.add(new_tube)
        db.session.commit()
        return new_tube

    @ns.expect(tube_info)
    @ns.marshal_with(tube_info)
    def patch(self):
        tube_inst = db.session.query(Tube).filter(Tube.barcode == api.payload['barcode']).one_or_none()
        if not tube_inst:
            return 404
        else:
            tube_inst.status = api.payload['status']
            # ORM takes care of the save when you commit
            db.session.commit()
            return tube_inst
