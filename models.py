from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Add a naming convention for database constraints
naming_convention = {
    "ix": "ix_%(table_name)s_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), nullable=False, unique=True)
    make_model = db.Column(db.String(100), nullable=False)
    individual_name = db.Column(db.String(100), nullable=False)


class WhitelistEntry(db.Model):
    __tablename__ = 'whitelist_entries'

    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), nullable=False)
    make_model = db.Column(db.String(100), nullable=False)
    individual_name = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete='CASCADE'), nullable=True)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date, nullable=False)
    effective_start_date = db.Column(db.Date, nullable=True)
    effective_end_date = db.Column(db.Date, nullable=True)

    company = db.relationship('Company', backref=db.backref('whitelist_entries', lazy=True))


class BlacklistEntry(db.Model):
    __tablename__ = 'blacklist_entries'

    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), nullable=False)
    make_model = db.Column(db.String(100), nullable=False)
    individual_name = db.Column(db.String(100), nullable=False)
    blacklisted_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(200), nullable=True)