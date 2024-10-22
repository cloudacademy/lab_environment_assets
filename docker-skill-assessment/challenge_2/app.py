import os
import psycopg

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_NAME = os.environ['DB_NAME']
DB_PASS = os.environ['DB_PASS']
DB_DATA = os.environ.get('DB_DATA', '100')


# Connect to an existing database
with psycopg.connect(f"host={DB_HOST} user={DB_USER} dbname={DB_NAME} password={DB_PASS}" ) as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rainbow (
                rid SERIAL PRIMARY KEY,
                num INTEGER
            )
            """)


        cur.execute("TRUNCATE TABLE rainbow")
        cur.execute(
            "INSERT INTO rainbow (num) VALUES (%s)",
            (DB_DATA,)
        )

        # Make the changes to the database persistent
        conn.commit()

        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM rainbow")
        print(f"Found: {cur.fetchone()[1]}")

