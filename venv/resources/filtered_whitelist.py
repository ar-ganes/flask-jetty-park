from flask import request
from flask_restful import Resource
from models import db, WhitelistEntry


class FilteredWhitelistResource(Resource):
    def get(self):
        print("Request Method:", request.method)
        print("Request Headers:", request.headers)
        print("Request Content-Type:", request.headers.get("Content-Type"))
        print("Query Parameters:", request.args)

        # Extract query parameters
        id = request.args.get('id', None)
        company_name = request.args.get('company_name', None)
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        sort_by = request.args.get('sort_by', None)
        sort_order = request.args.get('sort_order', 'asc')

        try:
            # Base query
            query = db.session.query(WhitelistEntry)

            # Filter by id if provided
            if id:
                query = query.filter(WhitelistEntry.id == id)

            # Filter by company_name if provided
            if company_name:
                query = query.filter(WhitelistEntry.company_name.ilike(f"%{company_name}%"))

            # Apply date range filters if provided
            if start_date:
                query = query.filter(WhitelistEntry.valid_from >= start_date)
            if end_date:
                query = query.filter(WhitelistEntry.valid_to <= end_date)

            # Apply sorting if specified
            if sort_by:
                if sort_by == 'license_plate':
                    sort_column = WhitelistEntry.license_plate
                elif sort_by == 'individual_name':
                    sort_column = WhitelistEntry.individual_name
                elif sort_by == 'valid_date':
                    sort_column = WhitelistEntry.valid_from
                else:
                    sort_column = None

                if sort_column:
                    sort_order = sort_column.asc() if sort_order == 'asc' else sort_column.desc()
                    query = query.order_by(sort_order)

            # Execute the query
            results = query.all()

            # Format the response
            response = [
                {
                    'id': entry.id,
                    'license_plate': entry.license_plate,
                    'make_model': entry.make_model,
                    'individual_name': entry.individual_name,
                    'company_name': entry.company_name,
                    'valid_from': entry.valid_from.strftime('%Y-%m-%d'),
                    'valid_to': entry.valid_to.strftime('%Y-%m-%d')
                }
                for entry in results
            ]

            return response, 200
        except Exception as e:
            print("Error:", e)
            return {"message": "Internal Server Error", "error": str(e)}, 500
