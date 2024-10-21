# Note: the module name is psycopg, not psycopg3
import psycopg

print('Buckle up, we are about to connect to a database!')

# Connect to an existing database
with psycopg.connect("dbname=appdb user=app-user password=secret host=postgres") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table
        cur.execute("""
            CREATE TABLE rainbow (
                rid SERIAL PRIMARY KEY,
                num INTEGER
            )
            """)

        cur.execute(
            "INSERT INTO rainbow (num) VALUES (%s)",
            (100,)
        )

        # Make the changes to the database persistent
        conn.commit()

        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM rainbow")
        print(cur.fetchone())

print('We are done here!')

        