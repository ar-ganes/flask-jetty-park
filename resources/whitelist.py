from flask_restful import Resource, reqparse
from models import db, WhitelistEntry
from flask import request, jsonify
from datetime import datetime
import logging

logging.basicConfig(level=logging.ERROR)

class WhitelistResource(Resource):
    def get(self):
        try:
            # Extract query parameters
            company_name = request.args.get('company_name')
            effective_start_date = request.args.get('effective_start_date')
            effective_end_date = request.args.get('effective_end_date')
            valid_start_date = request.args.get('valid_start_date')
            valid_end_date = request.args.get('valid_end_date')

            # Base query
            query = WhitelistEntry.query

            # Filter by company name
            if company_name:
                query = query.filter(WhitelistEntry.company_name.ilike(f"%{company_name}%"))

            # Apply date range filters
            if effective_start_date:
                effective_start_date = datetime.strptime(effective_start_date, '%Y-%m-%d').date()
                query = query.filter(WhitelistEntry.effective_start_date >= effective_start_date)
            if effective_end_date:
                effective_end_date = datetime.strptime(effective_end_date, '%Y-%m-%d').date()
                query = query.filter(WhitelistEntry.effective_end_date <= effective_end_date)
            if valid_start_date:
                valid_start_date = datetime.strptime(valid_start_date, '%Y-%m-%d').date()
                query = query.filter(WhitelistEntry.valid_from >= valid_start_date)
            if valid_end_date:
                valid_end_date = datetime.strptime(valid_end_date, '%Y-%m-%d').date()
                query = query.filter(WhitelistEntry.valid_to <= valid_end_date)

            # Fetch entries
            entries = query.all()

            # Format response
            response = [
                {
                    'license_plate': entry.license_plate,
                    'make_model': entry.make_model,
                    'individual_name': entry.individual_name,
                    'company_name': entry.company_name,
                    'valid_from': entry.valid_from.strftime('%Y-%m-%d') if entry.valid_from else None,
                    'valid_to': entry.valid_to.strftime('%Y-%m-%d') if entry.valid_to else None,
                    'effective_start_date': entry.effective_start_date.strftime('%Y-%m-%d') if entry.effective_start_date else None,
                    'effective_end_date': entry.effective_end_date.strftime('%Y-%m-%d') if entry.effective_end_date else None
                }
                for entry in entries
            ]
            return jsonify(response)

        except Exception as e:
            logging.error("Error occurred: %s", e)
            return {"message": "Internal Server Error", "error": str(e)}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('license_plate', type=str, required=True, help="License plate is required")
        parser.add_argument('make_model', type=str, required=True, help="Make and model are required")
        parser.add_argument('individual_name', type=str, required=True, help="Individual name is required")
        parser.add_argument('company_name', type=str, required=True, help="Company name is required")
        parser.add_argument('valid_from', type=str, required=True, help="Valid from date is required")
        parser.add_argument('valid_to', type=str, required=True, help="Valid to date is required")
        parser.add_argument('effective_start_date', type=str, required=False, help="Effective start date is optional")
        parser.add_argument('effective_end_date', type=str, required=False, help="Effective end date is optional")
        args = parser.parse_args()

        try:
            # Convert date strings to datetime objects
            valid_from = datetime.strptime(args['valid_from'], '%Y-%m-%d').date()
            valid_to = datetime.strptime(args['valid_to'], '%Y-%m-%d').date()
            effective_start_date = datetime.strptime(args['effective_start_date'], '%Y-%m-%d').date() if args.get('effective_start_date') else None
            effective_end_date = datetime.strptime(args['effective_end_date'], '%Y-%m-%d').date() if args.get('effective_end_date') else None

            # Validate date ranges
            if valid_from > valid_to:
                return {"error": "'valid_from' must be earlier than 'valid_to'"}, 400
            if effective_start_date and effective_end_date and effective_start_date > effective_end_date:
                return {"error": "'effective_start_date' must be earlier than 'effective_end_date'"}, 400

            # Create whitelist entry
            entry = WhitelistEntry(
                license_plate=args['license_plate'],
                make_model=args['make_model'],
                individual_name=args['individual_name'],
                company_name=args['company_name'],
                valid_from=valid_from,
                valid_to=valid_to,
                effective_start_date=effective_start_date,
                effective_end_date=effective_end_date
            )
            db.session.add(entry)
            db.session.commit()

            return {"message": "Vehicle whitelisted successfully"}, 201

        except Exception as e:
            db.session.rollback()
            logging.error("Error occurred: %s", e)
            return {"message": "Internal Server Error", "error": str(e)}, 500
