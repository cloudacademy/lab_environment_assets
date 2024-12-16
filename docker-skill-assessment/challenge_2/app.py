import os
import psycopg

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_NAME = os.environ['DB_NAME']
DB_PASS = os.environ['DB_PASS']
DB_INIT = os.environ.get('DB_INIT', 0)

CONNECTION_STRING = f"host={DB_HOST} user={DB_USER} dbname={DB_NAME} password={DB_PASS}"


# Helper functions

# context manager to handle database connections
def conn_cursor():
    try:
        with psycopg.connect(CONNECTION_STRING) as conn:
            with conn.cursor() as cur:
                yield conn, cur 
    finally:
        pass

    
def table_filled() -> bool:
    with conn_cursor() as (_, cur):
        # Ensure the rainbow table is filled.
        cur.execute("""SELECT COUNT(*) FROM rainbow WHERE num BETWEEN 1 AND 39""")
        return cur.fetchone()[0] == 20


def ensure_init() -> None:
    if not bool(DB_INIT):
        return
    
    with conn_cursor() as (conn, cur):
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rainbow (
                rid SERIAL PRIMARY KEY,
                num INTEGER
            )
            """
        )

        if not table_filled():
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

ensure_init()

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