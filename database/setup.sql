-- Database setup for Moorgrundbuch

-- Create database (run this separately if needed)
-- CREATE DATABASE moorgrundbuch;

-- Create tables

-- Clusters
CREATE TABLE clusters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usage types
CREATE TABLE usage_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hydrological situations
CREATE TABLE hydrological_situations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Soil types
CREATE TABLE soil_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vegetation types
CREATE TABLE vegetation_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Institutions
CREATE TABLE institutions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100), -- University, Research Institute, Company, Government Agency, etc.
    address TEXT,
    city VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    phone VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Persons
CREATE TABLE persons (
    id SERIAL PRIMARY KEY,
    salutation VARCHAR(20),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    phone VARCHAR(50),
    email VARCHAR(255),
    iban VARCHAR(50),
    profession VARCHAR(100),
    institution_id INTEGER REFERENCES institutions(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Person institution history (for tracking institution changes)
CREATE TABLE person_institution_history (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES persons(id),
    institution_id INTEGER REFERENCES institutions(id),
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Land parcels
CREATE TABLE land_parcels (
    id SERIAL PRIMARY KEY,
    parcel_number VARCHAR(100) NOT NULL,
    area_size DECIMAL(10, 2), -- in square meters
    owner_id INTEGER REFERENCES persons(id),
    address TEXT,
    city VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    coordinates GEOMETRY(POLYGON),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Locations (Standorte)
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    coordinates GEOMETRY(POINT),
    cluster_id INTEGER REFERENCES clusters(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Location land parcels (many-to-many relationship)
CREATE TABLE location_land_parcels (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    land_parcel_id INTEGER REFERENCES land_parcels(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(location_id, land_parcel_id)
);

-- Location usage history
CREATE TABLE location_usage_history (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    usage_type_id INTEGER REFERENCES usage_types(id),
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Location hydrological situation history
CREATE TABLE location_hydrological_history (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    hydrological_situation_id INTEGER REFERENCES hydrological_situations(id),
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Location soil type history
CREATE TABLE location_soil_history (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    soil_type_id INTEGER REFERENCES soil_types(id),
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Location vegetation history
CREATE TABLE location_vegetation_history (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    vegetation_type_id INTEGER REFERENCES vegetation_types(id),
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Measurement equipment
CREATE TABLE measurement_equipment (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    serial_number VARCHAR(100),
    manufacturer VARCHAR(255),
    installation_date DATE,
    location_id INTEGER REFERENCES locations(id),
    description TEXT,
    status VARCHAR(50), -- Active, Inactive, Maintenance, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL, -- Cultivator, Owner, Tenant, Contact Person, Other
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Person location roles (many-to-many relationship with roles)
CREATE TABLE person_location_roles (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES persons(id),
    location_id INTEGER REFERENCES locations(id),
    role_id INTEGER REFERENCES roles(id),
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Journal entries for locations
CREATE TABLE location_journal (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    person_id INTEGER REFERENCES persons(id), -- Person who performed the action
    action_date DATE NOT NULL,
    action_type VARCHAR(100), -- Visit, Maintenance, Measurement, etc.
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Journal entries for persons
CREATE TABLE person_journal (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES persons(id),
    action_date DATE NOT NULL,
    action_type VARCHAR(100),
    location_id INTEGER REFERENCES locations(id), -- Optional, if action is related to a location
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users for authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    person_id INTEGER REFERENCES persons(id),
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial data for roles
INSERT INTO roles (name, description) VALUES
('Bewirtschafter', 'Person responsible for cultivating the land'),
('Eigentümer', 'Owner of the land'),
('Pächter', 'Tenant of the land'),
('Ansprechpartner', 'Contact person for the location'),
('Sonstiges', 'Other roles not covered by the main categories');

-- Create extension for PostGIS (for geographical data)
-- Note: This requires PostGIS to be installed on the server
CREATE EXTENSION IF NOT EXISTS postgis; 