import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from geoalchemy2 import Geometry
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/moorgrundbuch')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    Migrate(app, db)
    
    return db

# Define SQLAlchemy models based on our database schema
class Cluster(db.Model):
    __tablename__ = 'clusters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    locations = db.relationship('Location', backref='cluster', lazy=True)

class UsageType(db.Model):
    __tablename__ = 'usage_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HydrologicalSituation(db.Model):
    __tablename__ = 'hydrological_situations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SoilType(db.Model):
    __tablename__ = 'soil_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class VegetationType(db.Model):
    __tablename__ = 'vegetation_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Institution(db.Model):
    __tablename__ = 'institutions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(255))
    website = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    persons = db.relationship('Person', backref='institution', lazy=True)

class Person(db.Model):
    __tablename__ = 'persons'
    
    id = db.Column(db.Integer, primary_key=True)
    salutation = db.Column(db.String(20))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(255))
    iban = db.Column(db.String(50))
    profession = db.Column(db.String(100))
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='person', uselist=False, lazy=True)
    location_journals = db.relationship('LocationJournal', backref='person', lazy=True)
    person_journals = db.relationship('PersonJournal', backref='person', lazy=True)

class PersonInstitutionHistory(db.Model):
    __tablename__ = 'person_institution_history'
    
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    person = db.relationship('Person', backref='institution_history')
    institution = db.relationship('Institution', backref='person_history')

class LandParcel(db.Model):
    __tablename__ = 'land_parcels'
    
    id = db.Column(db.Integer, primary_key=True)
    parcel_number = db.Column(db.String(100), nullable=False)
    area_size = db.Column(db.Numeric(10, 2))
    owner_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    coordinates = db.Column(Geometry('POLYGON'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = db.relationship('Person', backref='owned_parcels')

class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    coordinates = db.Column(Geometry('POINT'))
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    land_parcels = db.relationship('LandParcel', secondary='location_land_parcels', backref='locations')
    measurement_equipment = db.relationship('MeasurementEquipment', backref='location', lazy=True)
    location_journals = db.relationship('LocationJournal', backref='location', lazy=True)

class LocationLandParcel(db.Model):
    __tablename__ = 'location_land_parcels'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    land_parcel_id = db.Column(db.Integer, db.ForeignKey('land_parcels.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('location_id', 'land_parcel_id'),)

class LocationUsageHistory(db.Model):
    __tablename__ = 'location_usage_history'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    usage_type_id = db.Column(db.Integer, db.ForeignKey('usage_types.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    location = db.relationship('Location', backref='usage_history')
    usage_type = db.relationship('UsageType')

class LocationHydrologicalHistory(db.Model):
    __tablename__ = 'location_hydrological_history'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    hydrological_situation_id = db.Column(db.Integer, db.ForeignKey('hydrological_situations.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    location = db.relationship('Location', backref='hydrological_history')
    hydrological_situation = db.relationship('HydrologicalSituation')

class LocationSoilHistory(db.Model):
    __tablename__ = 'location_soil_history'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    soil_type_id = db.Column(db.Integer, db.ForeignKey('soil_types.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    location = db.relationship('Location', backref='soil_history')
    soil_type = db.relationship('SoilType')

class LocationVegetationHistory(db.Model):
    __tablename__ = 'location_vegetation_history'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    vegetation_type_id = db.Column(db.Integer, db.ForeignKey('vegetation_types.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    location = db.relationship('Location', backref='vegetation_history')
    vegetation_type = db.relationship('VegetationType')

class MeasurementEquipment(db.Model):
    __tablename__ = 'measurement_equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    manufacturer = db.Column(db.String(255))
    installation_date = db.Column(db.Date)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    description = db.Column(db.Text)
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PersonLocationRole(db.Model):
    __tablename__ = 'person_location_roles'
    
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    person = db.relationship('Person', backref='location_roles')
    location = db.relationship('Location', backref='person_roles')
    role = db.relationship('Role')

class LocationJournal(db.Model):
    __tablename__ = 'location_journal'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    action_date = db.Column(db.Date, nullable=False)
    action_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PersonJournal(db.Model):
    __tablename__ = 'person_journal'
    
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    action_date = db.Column(db.Date, nullable=False)
    action_type = db.Column(db.String(100))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    location = db.relationship('Location', backref='person_journals')

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 