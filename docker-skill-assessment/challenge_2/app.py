import os
import psycopg

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_NAME = os.environ['DB_NAME']
DB_PASS = os.environ['DB_PASS']
DB_INIT = os.environ.get('DB_INIT', 0)

CONNECTION_STRING = f"host={DB_HOST} user={DB_USER} dbname={DB_NAME} password={DB_PASS}"

if bool(DB_INIT):
    # Create the database, if it doesn't exist
    with psycopg.connect(CONNECTION_STRING) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Execute a command: this creates a new table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rainbow (
                    rid SERIAL PRIMARY KEY,
                    num INTEGER
                )
                """
            )

            cur.executemany("""INSERT INTO rainbow (num) VALUES (%s)""", [
                [1],
                [3],
                [5],
                [7],
                [9],
                [11],
                [13],
                [15],
                [17],
                [19],
                [21],
                [23],
                [25],
                [27],
                [29],
                [31],
                [33],
                [35],
                [37],
                [39],
            ])

            # Make the changes to the database persistent
            conn.commit()

###############################################################################

from flask import Flask

app = Flask(__name__)

@app.route("/")
def get_data():
    # Create the database, if it doesn't exist
    with psycopg.connect(CONNECTION_STRING) as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Execute a command: this creates a new table
            cur.execute("""SELECT num FROM rainbow""")
            # Join the results into a CSV string
            return ','.join([str(row[0]) for row in cur.fetchall()])