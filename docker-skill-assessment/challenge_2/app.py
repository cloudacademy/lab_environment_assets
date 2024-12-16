import os
from contextlib import contextmanager

import psycopg

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_NAME = os.environ['DB_NAME']
DB_PASS = os.environ['DB_PASS']
DB_INIT = os.environ.get('DB_INIT', 0)

CONNECTION_STRING = f"host={DB_HOST} user={DB_USER} dbname={DB_NAME} password={DB_PASS}"


@contextmanager
def con_cur():
    con = psycopg.connect(CONNECTION_STRING)
    cur = con.cursor()
    try:
        yield con, cur
    finally:
        cur.close()
        con.close()

    
def table_exists() -> bool:
    with con_cur() as (_, cur):
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'rainbow'
            )
            """
        )
        return cur.fetchone()[0]


def ensure_init() -> None:
    if not bool(DB_INIT):
        print("db-init: skipping")
        return
    
    if table_exists():
        print("db-init: table already exists")
        return
    
    with con_cur() as (conn, cur):
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

ensure_init()

app = Flask(__name__)

@app.route("/")
def get_data():
    with con_cur() as (_, cur):
        cur.execute("""SELECT num FROM rainbow""")
        return ','.join([str(row[0]) for row in cur.fetchall()])