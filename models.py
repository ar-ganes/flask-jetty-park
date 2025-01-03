from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    make_model = db.Column(db.String(100), nullable=False)
    individual_name = db.Column(db.String(100), nullable=False)

class WhitelistEntry(db.Model):
    __tablename__ = 'whitelist_entries'

    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), nullable=False)
    make_model = db.Column(db.String(100), nullable=False)
    individual_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=True)  # New field
    phone_number = db.Column(db.String(15), nullable=True)
    effective_start_date = db.Column(db.Date, nullable=True)  # Ensure this is defined
    effective_end_date = db.Column(db.Date, nullable=True)    # Ensure this is defined


class BlacklistEntry(db.Model):
    __tablename__ = 'blacklist_entries'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), nullable=False)
    make_model = db.Column(db.String(100), nullable=False)
    individual_name = db.Column(db.String(100), nullable=False)
    blacklisted_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(200), nullable=True)

