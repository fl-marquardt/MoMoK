import os
import sys
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, date
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection string from environment variable
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/moorgrundbuch')

def connect_to_db():
    """Connect to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connected to the database successfully!")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

def populate_clusters(conn):
    """Populate the clusters table with sample data"""
    cursor = conn.cursor()
    
    clusters = [
        ('Nordmoor', 'Moorgebiet im Norden'),
        ('Suedmoor', 'Moorgebiet im Sueden'),
        ('Ostmoor', 'Moorgebiet im Osten'),
        ('Westmoor', 'Moorgebiet im Westen'),
        ('Zentralmoor', 'Zentrales Moorgebiet')
    ]
    
    try:
        execute_values(
            cursor,
            "INSERT INTO clusters (name, description) VALUES %s RETURNING id",
            [(name, desc) for name, desc in clusters]
        )
        print(f"Added {len(clusters)} clusters")
        conn.commit()
    except Exception as e:
        print(f"Error adding clusters: {e}")
        conn.rollback()
    finally:
        cursor.close()

def populate_usage_types(conn):
    """Populate the usage_types table with sample data"""
    cursor = conn.cursor()
    
    usage_types = [
        ('Landwirtschaft', 'Landwirtschaftliche Nutzung'),
        ('Forstwirtschaft', 'Forstwirtschaftliche Nutzung'),
        ('Naturschutz', 'Naturschutzgebiet'),
        ('Renaturierung', 'Renaturierungsprojekt'),
        ('Torfabbau', 'Torfabbaugebiet'),
        ('Brache', 'Brachflaeche')
    ]
    
    try:
        execute_values(
            cursor,
            "INSERT INTO usage_types (name, description) VALUES %s RETURNING id",
            [(name, desc) for name, desc in usage_types]
        )
        print(f"Added {len(usage_types)} usage types")
        conn.commit()
    except Exception as e:
        print(f"Error adding usage types: {e}")
        conn.rollback()
    finally:
        cursor.close()

def populate_hydrological_situations(conn):
    """Populate the hydrological_situations table with sample data"""
    cursor = conn.cursor()
    
    hydrological_situations = [
        ('Nass', 'Dauerhaft nasse Bedingungen'),
        ('Feucht', 'Feuchte Bedingungen'),
        ('Wechselfeucht', 'Wechselnd feuchte Bedingungen'),
        ('Trocken', 'Trockene Bedingungen'),
        ('Ueberflutet', 'Zeitweise ueberflutet')
    ]
    
    try:
        execute_values(
            cursor,
            "INSERT INTO hydrological_situations (name, description) VALUES %s RETURNING id",
            [(name, desc) for name, desc in hydrological_situations]
        )
        print(f"Added {len(hydrological_situations)} hydrological situations")
        conn.commit()
    except Exception as e:
        print(f"Error adding hydrological situations: {e}")
        conn.rollback()
    finally:
        cursor.close()

def populate_soil_types(conn):
    """Populate the soil_types table with sample data"""
    cursor = conn.cursor()
    
    soil_types = [
        ('Hochmoortorf', 'Torf aus Hochmooren'),
        ('Niedermoortorf', 'Torf aus Niedermooren'),
        ('Anmoor', 'Anmooriger Boden'),
        ('Torfmudde', 'Torfmudde'),
        ('Mineralboden', 'Mineralischer Boden')
    ]
    
    try:
        execute_values(
            cursor,
            "INSERT INTO soil_types (name, description) VALUES %s RETURNING id",
            [(name, desc) for name, desc in soil_types]
        )
        print(f"Added {len(soil_types)} soil types")
        conn.commit()
    except Exception as e:
        print(f"Error adding soil types: {e}")
        conn.rollback()
    finally:
        cursor.close()

def populate_vegetation_types(conn):
    """Populate the vegetation_types table with sample data"""
    cursor = conn.cursor()
    
    vegetation_types = [
        ('Hochmoorvegetation', 'Typische Hochmoorvegetation'),
        ('Niedermoorvegetation', 'Typische Niedermoorvegetation'),
        ('Feuchtwiese', 'Feuchtwiese'),
        ('Erlenbruchwald', 'Erlenbruchwald'),
        ('Birkenbruchwald', 'Birkenbruchwald'),
        ('Schilf', 'Schilfbestand')
    ]
    
    try:
        execute_values(
            cursor,
            "INSERT INTO vegetation_types (name, description) VALUES %s RETURNING id",
            [(name, desc) for name, desc in vegetation_types]
        )
        print(f"Added {len(vegetation_types)} vegetation types")
        conn.commit()
    except Exception as e:
        print(f"Error adding vegetation types: {e}")
        conn.rollback()
    finally:
        cursor.close()

def populate_institutions(conn):
    """Populate the institutions table with sample data"""
    cursor = conn.cursor()
    
    institutions = [
        ('Universitaet Hamburg', 'University', 'Mittelweg 177', 'Hamburg', '20148', 'Deutschland', '+49 40 42838-0', 'info@uni-hamburg.de', 'www.uni-hamburg.de'),
        ('Landesamt fuer Umwelt Brandenburg', 'Government Agency', 'Seeburger Chaussee 2', 'Potsdam', '14476', 'Deutschland', '+49 33201 442-0', 'info@lfu.brandenburg.de', 'www.lfu.brandenburg.de'),
        ('NABU Deutschland', 'NGO', 'Charitestrasse 3', 'Berlin', '10117', 'Deutschland', '+49 30 284984-0', 'info@nabu.de', 'www.nabu.de'),
        ('Thuenen-Institut', 'Research Institute', 'Bundesallee 50', 'Braunschweig', '38116', 'Deutschland', '+49 531 596-0', 'info@thuenen.de', 'www.thuenen.de')
    ]
    
    try:
        execute_values(
            cursor,
            """
            INSERT INTO institutions 
            (name, type, address, city, postal_code, country, phone, email, website) 
            VALUES %s RETURNING id
            """,
            [(name, type_, address, city, postal, country, phone, email, website) 
             for name, type_, address, city, postal, country, phone, email, website in institutions]
        )
        print(f"Added {len(institutions)} institutions")
        conn.commit()
    except Exception as e:
        print(f"Error adding institutions: {e}")
        conn.rollback()
    finally:
        cursor.close()

def populate_persons(conn):
    """Populate the persons table with sample data"""
    cursor = conn.cursor()
    
    # First get institution IDs
    cursor.execute("SELECT id FROM institutions")
    institution_ids = [row[0] for row in cursor.fetchall()]
    
    if not institution_ids:
        print("No institutions found. Please populate institutions first.")
        return
    
    persons = [
        ('Herr', 'Hans', 'Mueller', 'Moorweg 12', 'Hamburg', '20148', 'Deutschland', '+49 176 12345678', 'hans.mueller@example.com', 'DE12345678901234567890', 'Biologe', institution_ids[0]),
        ('Frau', 'Maria', 'Schmidt', 'Torfstrasse 45', 'Berlin', '10117', 'Deutschland', '+49 176 87654321', 'maria.schmidt@example.com', 'DE09876543210987654321', 'Umweltwissenschaftlerin', institution_ids[1]),
        ('Herr', 'Klaus', 'Weber', 'Am Moor 3', 'Potsdam', '14476', 'Deutschland', '+49 176 23456789', 'klaus.weber@example.com', 'DE34567890123456789012', 'Landwirt', None),
        ('Frau', 'Sabine', 'Fischer', 'Moorheide 78', 'Braunschweig', '38116', 'Deutschland', '+49 176 98765432', 'sabine.fischer@example.com', 'DE21098765432109876543', 'Forstwirtin', institution_ids[3])
    ]
    
    try:
        execute_values(
            cursor,
            """
            INSERT INTO persons 
            (salutation, first_name, last_name, address, city, postal_code, country, phone, email, iban, profession, institution_id) 
            VALUES %s RETURNING id
            """,
            [(salutation, first_name, last_name, address, city, postal, country, phone, email, iban, profession, inst_id) 
             for salutation, first_name, last_name, address, city, postal, country, phone, email, iban, profession, inst_id in persons]
        )
        print(f"Added {len(persons)} persons")
        conn.commit()
    except Exception as e:
        print(f"Error adding persons: {e}")
        conn.rollback()
    finally:
        cursor.close()

def populate_land_parcels(conn):
    """Populate the land_parcels table with sample data"""
    cursor = conn.cursor()
    
    # First get person IDs for owners
    cursor.execute("SELECT id FROM persons")
    person_ids = [row[0] for row in cursor.fetchall()]
    
    if not person_ids:
        print("No persons found. Please populate persons first.")
        return
    
    # Sample land parcels with WKT (Well-Known Text) for polygon geometries
    land_parcels = [
        ('123/45', 10000.50, person_ids[0], 'Moorstrasse 1', 'Hamburg', '20148', 'Deutschland', 
         'POLYGON((10 10, 10 20, 20 20, 20 10, 10 10))'),
        ('234/56', 5000.75, person_ids[1], 'Torfweg 2', 'Berlin', '10117', 'Deutschland', 
         'POLYGON((30 30, 30 40, 40 40, 40 30, 30 30))'),
        ('345/67', 7500.25, person_ids[2], 'Moorheide 3', 'Potsdam', '14476', 'Deutschland', 
         'POLYGON((50 50, 50 60, 60 60, 60 50, 50 50))'),
        ('456/78', 12000.00, person_ids[3], 'Am Moor 4', 'Braunschweig', '38116', 'Deutschland', 
         'POLYGON((70 70, 70 80, 80 80, 80 70, 70 70))')
    ]
    
    try:
        for parcel in land_parcels:
            parcel_number, area_size, owner_id, address, city, postal_code, country, wkt = parcel
            
            cursor.execute(
                """
                INSERT INTO land_parcels 
                (parcel_number, area_size, owner_id, address, city, postal_code, country, coordinates) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))
                RETURNING id
                """,
                (parcel_number, area_size, owner_id, address, city, postal_code, country, wkt)
            )
        
        print(f"Added {len(land_parcels)} land parcels")
        conn.commit()
    except Exception as e:
        print(f"Error adding land parcels: {e}")
        conn.rollback()
    finally:
        cursor.close()

def populate_locations(conn):
    """Populate the locations table with sample data"""
    cursor = conn.cursor()
    
    # First get cluster IDs
    cursor.execute("SELECT id FROM clusters")
    cluster_ids = [row[0] for row in cursor.fetchall()]
    
    if not cluster_ids:
        print("No clusters found. Please populate clusters first.")
        return
    
    # Sample locations with WKT (Well-Known Text) for point geometries
    locations = [
        ('Nordmoor-Standort 1', 'Messstandort im noerdlichen Moorgebiet', 'POINT(10.5 53.5)', cluster_ids[0]),
        ('Suedmoor-Standort 1', 'Messstandort im suedlichen Moorgebiet', 'POINT(13.5 52.5)', cluster_ids[1]),
        ('Ostmoor-Standort 1', 'Messstandort im oestlichen Moorgebiet', 'POINT(14.0 52.0)', cluster_ids[2]),
        ('Westmoor-Standort 1', 'Messstandort im westlichen Moorgebiet', 'POINT(9.5 53.0)', cluster_ids[3]),
        ('Zentralmoor-Standort 1', 'Messstandort im zentralen Moorgebiet', 'POINT(12.0 52.5)', cluster_ids[4])
    ]
    
    try:
        for location in locations:
            name, description, wkt, cluster_id = location
            
            cursor.execute(
                """
                INSERT INTO locations 
                (name, description, coordinates, cluster_id) 
                VALUES (%s, %s, ST_GeomFromText(%s, 4326), %s)
                RETURNING id
                """,
                (name, description, wkt, cluster_id)
            )
        
        print(f"Added {len(locations)} locations")
        conn.commit()
    except Exception as e:
        print(f"Error adding locations: {e}")
        conn.rollback()
    finally:
        cursor.close()

def populate_location_land_parcels(conn):
    """Populate the location_land_parcels table with sample data"""
    cursor = conn.cursor()
    
    # Get location IDs
    cursor.execute("SELECT id FROM locations")
    location_ids = [row[0] for row in cursor.fetchall()]
    
    # Get land parcel IDs
    cursor.execute("SELECT id FROM land_parcels")
    land_parcel_ids = [row[0] for row in cursor.fetchall()]
    
    if not location_ids or not land_parcel_ids:
        print("No locations or land parcels found. Please populate them first.")
        return
    
    # Create some relationships between locations and land parcels
    # For simplicity, we'll just match them one-to-one for the first few
    relationships = []
    for i in range(min(len(location_ids), len(land_parcel_ids))):
        relationships.append((location_ids[i], land_parcel_ids[i]))
    
    try:
        execute_values(
            cursor,
            """
            INSERT INTO location_land_parcels 
            (location_id, land_parcel_id) 
            VALUES %s
            """,
            relationships
        )
        print(f"Added {len(relationships)} location-land parcel relationships")
        conn.commit()
    except Exception as e:
        print(f"Error adding location-land parcel relationships: {e}")
        conn.rollback()
    finally:
        cursor.close()

def populate_location_usage_history(conn):
    """Populate the location_usage_history table with sample data"""
    cursor = conn.cursor()
    
    # Get location IDs
    cursor.execute("SELECT id FROM locations")
    location_ids = [row[0] for row in cursor.fetchall()]
    
    # Get usage type IDs
    cursor.execute("SELECT id FROM usage_types")
    usage_type_ids = [row[0] for row in cursor.fetchall()]
    
    if not location_ids or not usage_type_ids:
        print("No locations or usage types found. Please populate them first.")
        return
    
    # Create usage history entries
    usage_history = [
        (location_ids[0], usage_type_ids[0], date(2010, 1, 1), date(2015, 12, 31)),
        (location_ids[0], usage_type_ids[2], date(2016, 1, 1), None),  # Current usage
        (location_ids[1], usage_type_ids[1], date(2012, 1, 1), date(2018, 6, 30)),
        (location_ids[1], usage_type_ids[3], date(2018, 7, 1), None),  # Current usage
        (location_ids[2], usage_type_ids[4], date(2005, 1, 1), date(2020, 12, 31)),
        (location_ids[2], usage_type_ids[3], date(2021, 1, 1), None)   # Current usage
    ]
    
    try:
        execute_values(
            cursor,
            """
            INSERT INTO location_usage_history 
            (location_id, usage_type_id, start_date, end_date) 
            VALUES %s
            """,
            usage_history
        )
        print(f"Added {len(usage_history)} location usage history entries")
        conn.commit()
    except Exception as e:
        print(f"Error adding location usage history: {e}")
        conn.rollback()
    finally:
        cursor.close()

def main():
    """Main function to populate the database"""
    conn = connect_to_db()
    
    try:
        # Populate reference tables
        populate_clusters(conn)
        populate_usage_types(conn)
        populate_hydrological_situations(conn)
        populate_soil_types(conn)
        populate_vegetation_types(conn)
        populate_institutions(conn)
        populate_persons(conn)
        
        # Populate main data tables
        populate_land_parcels(conn)
        populate_locations(conn)
        populate_location_land_parcels(conn)
        populate_location_usage_history(conn)
        
        print("Database populated successfully!")
    except Exception as e:
        print(f"Error populating database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main() 