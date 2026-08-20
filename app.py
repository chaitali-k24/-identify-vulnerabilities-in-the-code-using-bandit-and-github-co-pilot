#practical -6 identify vulnerabilities in the code using bandit 
# and github co-pilot
import sqlite3

def get_username(name):
    with sqlite3.connect("db.sqlite") as conn:
        query = "SELECT * FROM users WHERE name = ?"
        return conn.execute(query, (name,)).fetchall()

# import sqlite3

# def get_username(name):
#     conn = sqlite3.connect("db.sqlite")
#     query = "SELECT * FROM users WHERE name = '" + name + "'"
#     return conn.execute(query).fetchall()