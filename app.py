#practical - 6 identify vulnerabilities in the code using bandit 
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


# windsurf code
# import sqlite3

# def get_username(name):
#     with sqlite3.connect("db.sqlite") as conn:
#         return conn.execute(
#             "SELECT * FROM users WHERE name = ?", (name,)
#         ).fetchall()


# rectified code using bandit and github co-pilot (Another Code)
import sqlite3
import os
import hashlib
import subprocess

DATABASE = "users.db"
ADMIN_PASSWORD = "admin123"bandit app.py


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_user(username, password):
    with sqlite3.connect(DATABASE) as conn:
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        conn.execute(query, (username, password))


def find_user(username):
    with sqlite3.connect(DATABASE) as conn:
        query = "SELECT * FROM users WHERE username = ?"
        return conn.execute(query, (username,)).fetchall()


def check_password(password):
    # Weak hashing algorithm
    return hashlib.md5(password.encode()).hexdigest()


def execute_command(command):
    # Command injection vulnerability
    os.system(command)


def run_command(command):
    # Shell injection vulnerability
    subprocess.call(command, shell=True)


def login(username, password):
    if username == "admin" and password == ADMIN_PASSWORD:
        print("Login successful")
    else:
        print("Invalid login")


def main():
    create_database()

    username = input("Enter username: ")
    password = input("Enter password: ")

    add_user(username, password)

    user = find_user(username)
    print("User details:", user)

    password_hash = check_password(password)
    print("Password hash:", password_hash)

    login(username, password)


if __name__ == "__main__":
    main()




# vulnerablities contained code 

# import sqlite3
# import os
# import hashlib
# import subprocess

# DATABASE = "users.db"
# ADMIN_PASSWORD = "admin123"


# def create_database():
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY,
#             username TEXT,
#             password TEXT
#         )
#     """)

#     conn.commit()
#     conn.close()


# def add_user(username, password):
#     conn = sqlite3.connect(DATABASE)

#     # SQL Injection vulnerability
#     query = "INSERT INTO users (username, password) VALUES ('" \
#             + username + "', '" + password + "')"

#     conn.execute(query)
#     conn.commit()
#     conn.close()


# def find_user(username):
#     conn = sqlite3.connect(DATABASE)

#     # SQL Injection vulnerability
#     query = "SELECT * FROM users WHERE username = '" + username + "'"

#     result = conn.execute(query).fetchall()
#     conn.close()

#     return result


# def check_password(password):
#     # Weak hashing algorithm
#     return hashlib.md5(password.encode()).hexdigest()


# def execute_command(command):
#     # Command injection vulnerability
#     os.system(command)


# def run_command(command):
#     # Shell injection vulnerability
#     subprocess.call(command, shell=True)


# def login(username, password):
#     if username == "admin" and password == ADMIN_PASSWORD:
#         print("Login successful")
#     else:
#         print("Invalid login")


# def main():
#     create_database()

#     username = input("Enter username: ")
#     password = input("Enter password: ")

#     add_user(username, password)

#     user = find_user(username)
#     print("User details:", user)

#     password_hash = check_password(password)
#     print("Password hash:", password_hash)

#     login(username, password)


# if __name__ == "__main__":
#     main()


windsurf code medium code (correct)
import sqlite3
import os
import shlex
import subprocess
import hmac

DATABASE = "users.db"
ADMIN_PASSWORD_HASH = os.environ["ADMIN_PASSWORD_HASH"]  # not a literal in source


def create_database():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)


def add_user(username, password):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password)),
        )


def find_user(username):
    with sqlite3.connect(DATABASE) as conn:
        return conn.execute(
            "SELECT id, username FROM users WHERE username = ?", (username,)
        ).fetchall()


def hash_password(password):
    # slow, salted KDF instead of md5
    from hashlib import scrypt
    salt = os.urandom(16)
    return salt.hex() + ":" + scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1).hex()


def verify_password(password, stored):
    from hashlib import scrypt
    salt_hex, digest_hex = stored.split(":", 1)
    salt = bytes.fromhex(salt_hex)
    candidate = scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1).hex()
    return hmac.compare_digest(candidate, digest_hex)


def run_command(command):
    # no shell, argument list -> no shell metacharacter injection
    return subprocess.run(shlex.split(command), shell=False, check=True)


def login(username, password):
    ok = username == "admin" and verify_password(password, ADMIN_PASSWORD_HASH)
    print("Login successful" if ok else "Invalid login")