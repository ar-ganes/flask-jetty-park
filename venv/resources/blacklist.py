from flask_restful import Resource, reqparse
from sqlalchemy import or_, and_
from flask import request
from models import db, BlacklistEntry

class BlacklistResource(Resource):
    def get(self):
        try:
            # Extract query parameters
            license_plate = request.args.get('license_plate')
            make_model = request.args.get('make_model')
            individual_name = request.args.get('individual_name')
            sort_by = request.args.get('sort_by')  # Options: 'make_model', 'individual_name'
            sort_order = request.args.get('sort_order', 'asc')  # Default: 'asc'

            # Base query
            query = BlacklistEntry.query

            # Apply filters
            if license_plate:
                query = query.filter(BlacklistEntry.license_plate.ilike(f"%{license_plate}%"))
            if make_model:
                query = query.filter(BlacklistEntry.make_model.ilike(f"%{make_model}%"))
            if individual_name:
                query = query.filter(BlacklistEntry.individual_name.ilike(f"%{individual_name}%"))

            # Apply sorting
            if sort_by:
                if sort_by == 'make_model':
                    sort_column = BlacklistEntry.make_model
                elif sort_by == 'individual_name':
                    sort_column = BlacklistEntry.individual_name
                else:
                    return {"message": "Invalid sort_by parameter"}, 400

                sort_column = sort_column.asc() if sort_order == 'asc' else sort_column.desc()
                query = query.order_by(sort_column)

            # Execute query
            entries = query.all()

            # Format response
            response = {
                'total_blacklisted_vehicles': len(entries),
                'vehicles': [
                    {
                        'license_plate': entry.license_plate,
                        'make_model': entry.make_model,
                        'individual_name': entry.individual_name,
                        'blacklisted_date': entry.blacklisted_date.strftime('%Y-%m-%d') if entry.blacklisted_date else None,
                        'reason': entry.reason
                    }
                    for entry in entries
                ]
            }

            return response, 200
        except Exception as e:
            print("Error:", e)
            return {"message": "Internal Server Error", "error": str(e)}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('license_plate', type=str, required=True, help="License plate is required")
        parser.add_argument('make_model', type=str, required=True, help="Vehicle make and model are required")
        parser.add_argument('individual_name', type=str, required=True, help="Individual name is required")
        parser.add_argument('blacklisted_date', type=str, required=True, help="Blacklisted date is required (YYYY-MM-DD)")
        parser.add_argument('reason', type=str, required=False, help="Reason for blacklisting")
        args = parser.parse_args()

        try:
            # Debug log for arguments
            print("Arguments received:", args)

            # Create a new blacklist entry
            entry = BlacklistEntry(
                license_plate=args['license_plate'],
                make_model=args['make_model'],
                individual_name=args['individual_name'],
                blacklisted_date=args['blacklisted_date'],
                reason=args.get('reason')
            )
            db.session.add(entry)
            db.session.commit()

            return {"message": "Vehicle successfully blacklisted"}, 201

        except Exception as e:
            db.session.rollback()
            print("Error:", e)
            return {"message": "Internal Server Error", "error": str(e)}, 500