# db_diagnostic.py
import os
import sys
import psycopg2
from dotenv import load_dotenv, find_dotenv
import inspect

# Print current working directory and script location
print(f"Current working directory: {os.getcwd()}")
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)
print(f"Script location: {script_path}")

# Try to find .env file
dotenv_path = find_dotenv(usecwd=True)
print(f".env file found at: {dotenv_path if dotenv_path else 'Not found'}")

# Load environment variables from .env file
load_dotenv(dotenv_path=dotenv_path, override=True)

# Print all environment variables (excluding sensitive ones)
print("\nEnvironment variables:")
for key, value in os.environ.items():
    if key.lower() not in ['database_url', 'password', 'secret_key']:
        print(f"  {key}={value}")
    else:
        print(f"  {key}={'*' * 8} (masked for security)")

# Get database connection string from .env
db_url = os.getenv('DATABASE_URL')
print(f"\nDatabase URL from .env: {db_url if db_url else 'Not found'}")

if not db_url:
    print("ERROR: DATABASE_URL not found in .env file")
    sys.exit(1)

# Parse the connection string
# Format: postgresql://username:password@host:port/dbname
try:
    # Simple parsing of the connection string
    parts = db_url.replace('postgresql://', '').split('@')
    user_pass = parts[0].split(':')
    host_port_db = parts[1].split('/')
    host_port = host_port_db[0].split(':')
    
    username = user_pass[0]
    password = user_pass[1]
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 5432
    dbname = host_port_db[1]
    
    print(f"Parsed connection details:")
    print(f"  Username: {username}")
    print(f"  Password: {password}")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  Database: {dbname}")
except Exception as e:
    print(f"ERROR: Failed to parse DATABASE_URL: {e}")
    sys.exit(1)

# Test PostgreSQL connection
print("\nTesting PostgreSQL connection...")
try:
    # First try to connect to PostgreSQL server without specifying a database
    conn = psycopg2.connect(
        user=username,
        password=password,
        host=host,
        port=port
    )
    conn.close()
    print("✓ Successfully connected to PostgreSQL server")
except Exception as e:
    print(f"✗ Failed to connect to PostgreSQL server: {e}")
    print("  Please check if PostgreSQL is running and credentials are correct")
    sys.exit(1)

# Test connection to the specific database
print(f"\nTesting connection to database '{dbname}'...")
try:
    conn = psycopg2.connect(
        user=username,
        password=password,
        host=host,
        port=port,
        dbname=dbname
    )
    conn.close()
    print(f"✓ Successfully connected to database '{dbname}'")
except Exception as e:
    print(f"✗ Failed to connect to database '{dbname}': {e}")
    print("  The database might not exist. Do you want to create it? (y/n)")
    choice = input().lower()
    if choice == 'y':
        try:
            # Connect to 'postgres' database to create our target database
            conn = psycopg2.connect(
                user=username,
                password=password,
                host=host,
                port=port,
                dbname='postgres'
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {dbname}")
            cursor.close()
            conn.close()
            print(f"✓ Database '{dbname}' created successfully")
        except Exception as e:
            print(f"✗ Failed to create database: {e}")
            sys.exit(1)
    else:
        print("Database creation skipped")
        sys.exit(1)

# Test PostGIS extension
print("\nChecking PostGIS extension...")
try:
    conn = psycopg2.connect(
        user=username,
        password=password,
        host=host,
        port=port,
        dbname=dbname
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT PostGIS_version()")
    version = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    print(f"✓ PostGIS extension is installed (version: {version})")
except Exception as e:
    print(f"✗ PostGIS extension check failed: {e}")
    print("  Do you want to install PostGIS extension? (y/n)")
    choice = input().lower()
    if choice == 'y':
        try:
            conn = psycopg2.connect(
                user=username,
                password=password,
                host=host,
                port=port,
                dbname=dbname
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
            cursor.close()
            conn.close()
            print("✓ PostGIS extension installed successfully")
        except Exception as e:
            print(f"✗ Failed to install PostGIS extension: {e}")
            print("  You may need to install PostGIS on your system first")
            sys.exit(1)
    else:
        print("PostGIS installation skipped")
        print("WARNING: Your application requires PostGIS for spatial data")

print("\nDiagnostic completed. If all checks passed, your database connection should work.")