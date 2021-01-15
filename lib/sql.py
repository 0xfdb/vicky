# Sql Module (lib/sql.py)

import sqlite3

# Some sql functions
def list_from_db(database, query, tup):
    with sqlite3.connect(database) as conn:
        cur = conn.cursor()
        cur.execute(query, tup)
        return cur.fetchall()

def add_to_db(database, sqlcmd, tup):
    with sqlite3.connect(database) as conn:
        cur = conn.cursor()
        cur.execute(query, tup)
        conn.commit()
