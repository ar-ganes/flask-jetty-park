from flask import Flask
from flask_restful import Api
from models import db
from config import Config
from resources.whitelist import WhitelistResource
from resources.blacklist import BlacklistResource

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy (without Flask-Migrate for now)
db.init_app(app)

# Initialize Flask-RESTful API
api = Api(app)
api.add_resource(WhitelistResource, '/whitelist')
api.add_resource(BlacklistResource, '/blacklist')

print("Database URI:", Config.SQLALCHEMY_DATABASE_URI)



if __name__ == '__main__':
    app.run(debug=True)
