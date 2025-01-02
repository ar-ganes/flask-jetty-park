from flask import Flask
from flask_restful import Api
from models import db
from config import Config
from flask_cors import CORS
from resources.whitelist import WhitelistResource
from resources.blacklist import BlacklistResource

app = Flask(__name__)
CORS(app) 
app.config.from_object(Config)

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