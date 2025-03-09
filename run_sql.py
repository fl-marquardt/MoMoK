import psycopg2

# Hard-coded connection string to avoid any encoding issues
conn_string = "host=localhost port=5432 dbname=moorgrundbuch user=postgres password=admin"

def main():
    """Run the SQL file to populate the database"""
    conn = None
    cursor = None
    
    try:
        # Connect to the database
        print("Connecting to database...")
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        # Read the SQL file
        print("Reading SQL file...")
        with open('populate.sql', 'r') as f:
            sql = f.read()
        
        # Execute the SQL
        print("Executing SQL...")
        cursor.execute(sql)
        
        # Commit the transaction
        conn.commit()
        print("Database populated successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main() 