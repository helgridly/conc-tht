from flask_sqlalchemy import SQLAlchemy
import enum
from flask_restx import Api, Resource, fields

db = SQLAlchemy()

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
        """Override so these display as e.g. `registered` rather than `TubeStatus.registered`"""
        return self.name


class Tube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.Enum(TubeStatus), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey(Patient.id), nullable=False)

    @classmethod
    def get_model(cls):
        return {
            "barcode": fields.String(example="uuid-12345"),
            "status": fields.String(enum = [e.name for e in TubeStatus])
        }
