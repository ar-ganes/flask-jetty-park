from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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



class Fares(db.Model):
    __tablename__ = 'fares'

    fareid = db.Column(db.Integer, primary_key=True)
    fareamount = db.Column(db.Float, nullable=False)
    categoryid = db.Column(db.BigInteger, nullable=True)
    routename = db.Column(db.String, nullable=True)
    isactive = db.Column(db.Boolean, default=True)
    validtill = db.Column(db.DateTime, default=datetime.utcnow)
    createddate = db.Column(db.DateTime, default=datetime.utcnow)
    createdby = db.Column(db.String, nullable=True)
    lastupdateddate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lastupdatedby = db.Column(db.String, nullable=True)
    agencyid = db.Column(db.Integer, nullable=True)
    serverdate = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String, nullable=True)
    expirytime = db.Column(db.DateTime, nullable=True)
    zoneid = db.Column(db.BigInteger, nullable=True)
    farename = db.Column(db.String, nullable=True)
    maxcount = db.Column(db.Integer, nullable=True)
    productdescription = db.Column(db.String, nullable=True)
    productmiscdescription = db.Column(db.String, nullable=True)
    verificationstatus = db.Column(db.Integer, nullable=True)
    paymentmode = db.Column(db.Integer, nullable=True)
    productname = db.Column(db.String, nullable=True)
    productcost = db.Column(db.Float, nullable=True)
    productvegcategory = db.Column(db.Integer, nullable=True)
    productimageurl = db.Column(db.String, nullable=True)
    reactivation_count = db.Column(db.Integer, nullable=True)
    reactivation_interval = db.Column(db.Integer, nullable=True)
    reactivation_status = db.Column(db.Boolean, default=False)
    hours = db.Column(db.Integer, nullable=True)
    days = db.Column(db.Integer, nullable=True)
    months = db.Column(db.Integer, nullable=True)
    expiry_days = db.Column(db.Integer, nullable=True)
    v_minutes = db.Column(db.Integer, nullable=True)
    v_hours = db.Column(db.Integer, nullable=True)
    v_days = db.Column(db.Integer, nullable=True)
    v_months = db.Column(db.Integer, nullable=True)
    devicecode = db.Column(db.Integer, nullable=True)
    ski = db.Column(db.String, nullable=True)

