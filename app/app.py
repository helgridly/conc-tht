import flask
from flask_restx import Api, Resource, fields

import uuid

from app.db import db, Patient, TubeStatus, Tube

routes = flask.Blueprint('tube-service', __name__)
api = Api(routes, version='0.1', title='Tubes Service',
        description='tubes service',
        validate=True) # validate all payloads

ns = api.namespace('/', description='tube handling')



tube_info = ns.model("TubeInfo", Tube.get_model())
new_tube = ns.model('NewTube', {
    # this bonkers regex matches against emails, per https://www.emailregex.com/
    'patient_email': fields.String(
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        example = "test@example.com"
    )})

@ns.route("/tubes")
@ns.response(400, 'Validation Error')
class Tubes(Resource):
    @ns.marshal_list_with(tube_info)
    def get(self):
        """List all tubes in `registered` state."""
        tubes = db.session.query(Tube).filter(Tube.status == 'registered').all()
        return tubes

    @ns.expect(new_tube)
    @ns.marshal_with(tube_info)
    def post(self):
        """Add a new tube."""
        # Will create a new patient if the email doesn't already exist.
        new_tube = Tube()
        new_tube.barcode = str(uuid.uuid4())
        new_tube.status = "registered"
        new_tube.patient_id = Patient.get_or_create(api.payload['patient_email']).id
        db.session.add(new_tube)
        db.session.commit()
        return new_tube

    @ns.expect(tube_info)
    @ns.marshal_with(tube_info)
    @ns.response(404, "Barcode not found")
    def patch(self):
        """Update status of an existing tube."""
        tube_inst = db.session.query(Tube).filter(Tube.barcode == api.payload['barcode']).one_or_none()
        if not tube_inst:
            return 404
        else:
            tube_inst.status = api.payload['status']
            # ORM takes care of the save when you commit
            db.session.commit()
            return tube_inst
