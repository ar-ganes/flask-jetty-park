from flask_restful import Resource, reqparse
from models import WhitelistEntry

class UsageReportResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('company_id', type=int, required=True)
        parser.add_argument('start_date', type=str, required=True)
        parser.add_argument('end_date', type=str, required=True)
        args = parser.parse_args()

        entries = WhitelistEntry.query.filter_by(company_id=args['company_id']).all()
        report = [{"vehicle_id": e.vehicle_id, "valid_from": e.valid_from, "valid_to": e.valid_to} for e in entries]
        return {"report": report}
