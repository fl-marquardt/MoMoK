import os
import sys
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default connection parameters
DEFAULT_USER = "postgres"
DEFAULT_PASSWORD = "admin"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = "5432"
DEFAULT_DATABASE = "postgres"  # Default database to connect to initially

# Target database and user to create
TARGET_DATABASE = "moorgrundbuch"
TARGET_USER = "postgres"  # Using the same user for simplicity
TARGET_PASSWORD = "postgres"  # Using the same password for simplicity

def test_connection():
    """Test connection to PostgreSQL with default credentials"""
    conn_string = f"host={DEFAULT_HOST} port={DEFAULT_PORT} user={DEFAULT_USER} password={DEFAULT_PASSWORD} dbname={DEFAULT_DATABASE}"
    
    try:
        conn = psycopg2.connect(conn_string)
        print("Successfully connected to PostgreSQL!")
        conn.close()
        return True
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return False

def create_database():
    """Create the target database if it doesn't exist"""
    conn_string = f"host={DEFAULT_HOST} port={DEFAULT_PORT} user={DEFAULT_USER} password={DEFAULT_PASSWORD} dbname={DEFAULT_DATABASE}"
    
    try:
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{TARGET_DATABASE}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database '{TARGET_DATABASE}'...")
            cursor.execute(f"CREATE DATABASE {TARGET_DATABASE}")
            print(f"Database '{TARGET_DATABASE}' created successfully!")
        else:
            print(f"Database '{TARGET_DATABASE}' already exists.")
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def check_postgis():
    """Check if PostGIS extension is available and install it if possible"""
    conn_string = f"host={DEFAULT_HOST} port={DEFAULT_PORT} user={DEFAULT_USER} password={DEFAULT_PASSWORD} dbname={TARGET_DATABASE}"
    
    try:
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if PostGIS extension is available
        cursor.execute("SELECT 1 FROM pg_available_extensions WHERE name = 'postgis'")
        postgis_available = cursor.fetchone()
        
        if not postgis_available:
            print("PostGIS extension is not available in your PostgreSQL installation.")
            print("Please install PostGIS before continuing.")
            print("You can install it using:")
            print("  - Windows: Download and install from https://postgis.net/windows_downloads/")
            print("  - Linux: sudo apt-get install postgis")
            print("  - macOS: brew install postgis")
            return False
        
        # Try to create the extension
        print("Creating PostGIS extension...")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
        print("PostGIS extension created successfully!")
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error setting up PostGIS: {e}")
        return False

def setup_schema():
    """Set up the database schema using the setup.sql file"""
    conn_string = f"host={DEFAULT_HOST} port={DEFAULT_PORT} user={DEFAULT_USER} password={DEFAULT_PASSWORD} dbname={TARGET_DATABASE}"
    
    try:
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Read the SQL file
        with open('database/setup.sql', 'r') as f:
            sql_script = f.read()
        
        # Remove the PostGIS extension creation line since we've already done it
        sql_script = sql_script.replace('CREATE EXTENSION IF NOT EXISTS postgis;', '-- PostGIS extension already created')
        
        print("Setting up database schema...")
        cursor.execute(sql_script)
        print("Database schema set up successfully!")
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error setting up schema: {e}")
        return False

def update_env_file():
    """Update the .env file with the correct database connection string"""
    try:
        # Create the connection string
        conn_string = f"postgresql://{TARGET_USER}:{TARGET_PASSWORD}@{DEFAULT_HOST}:{DEFAULT_PORT}/{TARGET_DATABASE}"
        
        # Check if .env file exists
        if os.path.exists('.env'):
            # Read the current .env file
            with open('.env', 'r') as f:
                lines = f.readlines()
            
            # Update or add the DATABASE_URL line
            database_url_exists = False
            for i, line in enumerate(lines):
                if line.startswith('DATABASE_URL='):
                    lines[i] = f"DATABASE_URL={conn_string}\n"
                    database_url_exists = True
                    break
            
            if not database_url_exists:
                lines.append(f"DATABASE_URL={conn_string}\n")
            
            # Write the updated .env file
            with open('.env', 'w') as f:
                f.writelines(lines)
        else:
            # Create a new .env file
            with open('.env', 'w') as f:
                f.write(f"DATABASE_URL={conn_string}\n")
                f.write("SECRET_KEY=dev-key-for-development-only-change-in-production\n")
        
        print(f".env file updated with DATABASE_URL={conn_string}")
        return True
    except Exception as e:
        print(f"Error updating .env file: {e}")
        return False

def main():
    """Main function to set up PostgreSQL"""
    print("Testing connection to PostgreSQL...")
    if not test_connection():
        print("Failed to connect to PostgreSQL. Please check your PostgreSQL installation and credentials.")
        return False
    
    print("\nCreating database...")
    if not create_database():
        return False
    
    print("\nSetting up PostGIS extension...")
    if not check_postgis():
        return False
    
    print("\nSetting up schema...")
    if not setup_schema():
        return False
    
    print("\nUpdating .env file...")
    if not update_env_file():
        return False
    
    print("\nPostgreSQL setup completed successfully!")
    print(f"Database: {TARGET_DATABASE}")
    print(f"User: {TARGET_USER}")
    print(f"Password: {TARGET_PASSWORD}")
    print(f"Host: {DEFAULT_HOST}")
    print(f"Port: {DEFAULT_PORT}")
    print("You can now run your application with these credentials.")
    
    return True

if __name__ == "__main__":
    main() 