from flask import Flask, request, jsonify
from flask_restful import Api
from models import db
from config import Config
from flask_cors import CORS
from resources.whitelist import WhitelistResource
from resources.blacklist import BlacklistResource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import requests
import os
# Initialize JWTManager
 

app = Flask(__name__)
CORS(app) 
app.config.from_object(Config)

jwt = JWTManager(app)

# Hardcoded credentials (for simplicity)
USERNAME = "zigjettypark@zed.digital"
PASSWORD = "zigjettypark@1234"

@app.route('/login', methods=['POST'])
def login():
    # Parse the incoming JSON payload
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Username and password are required"}), 400

    # Validate username and password
    if data["username"] == USERNAME and data["password"] == PASSWORD:
        # Generate JWT token
        access_token = create_access_token(identity=data["username"])
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


CARDKNOX_BASE_URL = "https://x1.cardknox.com"

@app.route('/report', methods=['POST'])
def fetch_report():
    data = request.get_json()
    try:
        # Send the POST request using the requests library
        response = requests.post(f"{CARDKNOX_BASE_URL}/report", data=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reportjson', methods=['POST'])
def fetch_reportjson():
    data = request.get_json()
    try:
        # Send the POST request using the requests library
        response = requests.post(f"{CARDKNOX_BASE_URL}/reportjson", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Initialize SQLAlchemy (without Flask-Migrate for now)
db.init_app(app)

# Initialize Flask-RESTful API
api = Api(app)
api.add_resource(WhitelistResource, '/whitelist')
api.add_resource(BlacklistResource, '/blacklist')

if __name__ == '__main__':
    app.run(debug=True)



















''''from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from models import db
from config import Config
from resources.whitelist import WhitelistResource
from resources.blacklist import BlacklistResource
from resources.reports import UsageReportResource
from resources.filtered_whitelist import FilteredWhitelistResource

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Flask-RESTful API
api = Api(app)
api.add_resource(WhitelistResource, '/whitelist')
api.add_resource(BlacklistResource, '/blacklist')
api.add_resource(UsageReportResource, '/usage_report')
api.add_resource(FilteredWhitelistResource, '/filtered_whitelist') 

if __name__ == '__main__':
    app.run()'''