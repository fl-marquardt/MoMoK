import os
import sys
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection string from environment variable
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/moorgrundbuch')

# Parse the connection string to get components
# Format: postgresql://username:password@host:port/database
db_parts = DATABASE_URL.replace('postgresql://', '').split('/')
connection_parts = db_parts[0].split('@')
credentials = connection_parts[0].split(':')
host_port = connection_parts[1].split(':')

username = credentials[0]
password = credentials[1]
host = host_port[0]
port = host_port[1] if len(host_port) > 1 else '5432'
database = db_parts[1]

def create_database():
    """Create the database if it doesn't exist"""
    # Connect to default postgres database to create our database
    conn_string = f"host={host} port={port} user={username} password={password} dbname=postgres"
    
    try:
        # Connect to the default postgres database
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database '{database}'...")
            cursor.execute(f"CREATE DATABASE {database}")
            print(f"Database '{database}' created successfully!")
        else:
            print(f"Database '{database}' already exists.")
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def setup_schema():
    """Set up the database schema using the setup.sql file"""
    try:
        # Connect to our database
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Read the SQL file
        with open('database/setup.sql', 'r') as f:
            sql_script = f.read()
        
        print("Setting up database schema...")
        cursor.execute(sql_script)
        print("Database schema set up successfully!")
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error setting up schema: {e}")
        return False

def main():
    """Main function to create database and set up schema"""
    if create_database():
        if setup_schema():
            print("Database and schema setup completed successfully!")
            return True
    
    print("Database setup failed.")
    return False

if __name__ == "__main__":
    main() 