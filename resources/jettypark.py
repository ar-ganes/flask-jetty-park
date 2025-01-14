from flask_restful import Resource, reqparse
from flask import request
from models import db, Fares
from datetime import datetime

class FareResource(Resource):
    def get(self):
        try:
            # Extract query parameters
            agencyid = request.args.get('agencyid')
            if not agencyid:
                return {"message": "agencyid is required"}, 400

            # Query the database
            fares = Fares.query.filter_by(agencyid=agencyid).all()
            if not fares:
                return {"message": "No fares found for the given agencyid"}, 404

            # Prepare the response
            response = [
                {
                    "agencyid": fare.agencyid,
                    "bannerimage": "null",  # Placeholder if field is unavailable
                    "categoryid": fare.categoryid,
                    "categoryimage": "https://www.izig.app/img/app/ticket-01.png",  # Example static URL
                    "categoryname": "Tickets",  # Placeholder or static value
                    "createdby": fare.createdby,
                    "createddate": fare.createddate.isoformat() if fare.createddate else None,
                    "days": fare.days or 0,
                    "devicecode": fare.devicecode or 0,
                    "expirydays": fare.expiry_days or 0,
                    "expirytime": fare.expirytime.isoformat() if fare.expirytime else None,
                    "fareamount": fare.fareamount,
                    "fareid": fare.fareid,
                    "farename": fare.farename,
                    "hours": fare.hours or 0,
                    "isactive": fare.isactive,
                    "lastupdatedby": fare.lastupdatedby,
                    "lastupdateddate": fare.lastupdateddate.isoformat() if fare.lastupdateddate else None,
                    "maxcount": fare.maxcount or 0,
                    "months": fare.months or 0,
                    "paymentmode": fare.paymentmode or 0,
                    "productcost": fare.productcost,
                    "productdescription": fare.productdescription,
                    "productimageurl": fare.productimageurl,
                    "productmiscdescription": fare.productmiscdescription,
                    "productname": fare.productname,
                    "productvegcategory": fare.productvegcategory or 0,
                    "reactivationcount": fare.reactivation_count or 0,
                    "reactivationinterval": fare.reactivation_interval or 0,
                    "reactivationstatus": fare.reactivation_status,
                    "routename": fare.routename,
                    "season_end": fare.validtill.isoformat() if fare.validtill else None,
                    "season_start": fare.createddate.isoformat() if fare.createddate else None,
                    "serverdate": fare.serverdate.isoformat() if fare.serverdate else None,
                    "ski": fare.ski,  # Added the ski field here
                    "toll_trip_id": "0",  # Placeholder
                    "type": fare.type,
                    "v_days": fare.v_days or 0,
                    "v_hours": fare.v_hours or 0,
                    "v_minutes": fare.v_minutes or 0,
                    "v_months": fare.v_months or 0,
                    "validtill": fare.validtill.isoformat() if fare.validtill else None,
                    "verificationstatus": fare.verificationstatus or 0,
                    "zoneid": fare.zoneid or 0,
                    "isFavourite": fare.isfavourite,
                }
                for fare in fares
            ]

            return response, 200

        except Exception as e:
            print("Error:", e)
            return {"message": "Internal Server Error", "error": str(e)}, 500
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('agencyid', type=int, required=True, help="agencyid is required")
        parser.add_argument('fareamount', type=float, required=True, help="fareamount is required")
        parser.add_argument('farename', type=str, required=True, help="farename is required")
        parser.add_argument('validtill', type=str, required=False, help="validtill in YYYY-MM-DD format")
        parser.add_argument('ski', type=str, required=False, help="Optional field for ski")
        parser.add_argument('categoryid', type=int, required=False, help="Optional field for categoryid")
        parser.add_argument('routename', type=str, required=False, help="Optional field for routename")
        parser.add_argument('createdby', type=str, required=False, help="Optional field for createdby")
        parser.add_argument('productdescription', type=str, required=False, help="Optional field for productdescription")
        parser.add_argument('productcost', type=float, required=False, help="Optional field for productcost")
        parser.add_argument('isfavourite', type=bool, required=False, help="Optional field for isfavourite (True/False)")
        args = parser.parse_args()

        try:
            # Debug log to check parsed arguments
            print("Parsed Arguments:", args)

            # Handle `isfavourite` explicitly
            isfavourite_value = args.get('isfavourite', False)

            # Create a new Fare entry
            fare = Fares(
                agencyid=args['agencyid'],
                fareamount=args['fareamount'],
                farename=args['farename'],
                validtill=datetime.fromisoformat(args['validtill']) if args.get('validtill') else None,
                ski=args.get('ski'),
                categoryid=args.get('categoryid'),
                routename=args.get('routename'),
                createdby=args.get('createdby'),
                productdescription=args.get('productdescription'),
                productcost=args.get('productcost'),
                isfavourite=isfavourite_value
            )
            db.session.add(fare)
            db.session.commit()

            return {"message": "Fare created successfully", "fareid": fare.fareid}, 201

        except Exception as e:
            db.session.rollback()
            print("Error:", e)
            return {"message": "Internal Server Error", "error": str(e)}, 500

    
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fareid', type=int, required=True, help="fareid is required")
        parser.add_argument('fareamount', type=float, required=False)
        parser.add_argument('farename', type=str, required=False)
        parser.add_argument('validtill', type=str, required=False)
        parser.add_argument('ski', type=str, required=False)
        parser.add_argument('categoryid', type=int, required=False)
        parser.add_argument('routename', type=str, required=False)
        parser.add_argument('isactive', type=bool, required=False)
        parser.add_argument('expirytime', type=str, required=False)
        parser.add_argument('maxcount', type=int, required=False)
        parser.add_argument('productdescription', type=str, required=False)
        parser.add_argument('productcost', type=float, required=False)
        parser.add_argument('createdby', type=str, required=False)
        parser.add_argument('lastupdatedby', type=str, required=False)
        parser.add_argument('productname', type=str, required=False)
        parser.add_argument('productimageurl', type=str, required=False)
        parser.add_argument('isfavourite', type=bool, required=False)
        args = parser.parse_args()

        try:
            # Fetch the Fare entry to update
            fare = Fares.query.get(args['fareid'])
            if not fare:
                return {"message": "Fare not found"}, 404

            # Log parsed arguments for debugging
            print("Parsed Arguments:", args)

            # Dynamically update all fields present in args
            for field, value in args.items():
                if field != 'fareid' and value is not None:  # Skip fareid and None values
                    if field == 'validtill' or field == 'expirytime':  # Handle date fields
                        setattr(fare, field, datetime.fromisoformat(value))
                    else:
                        print(f"Updating field: {field}, Value: {value}")  # Debug log
                        setattr(fare, field, value)

            # Commit changes to the database
            db.session.commit()
            return {"message": "Fare updated successfully"}, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", e)
            return {"message": "Internal Server Error", "error": str(e)}, 500


    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fareid', type=int, required=True, help="fareid is required")
        args = parser.parse_args()

        try:
            # Fetch the Fare entry to delete
            fare = Fares.query.get(args['fareid'])
            if not fare:
                return {"message": "Fare not found"}, 404

            # Delete the entry
            db.session.delete(fare)
            db.session.commit()
            return {"message": "Fare deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", e)
            return {"message": "Internal Server Error", "error": str(e)}, 500

        
