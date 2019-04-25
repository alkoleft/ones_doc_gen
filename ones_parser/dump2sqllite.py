import sqlite3


conn = None


def get_connection():
    global conn

    if conn is None:
        conn = sqlite3.connect('data.db')
    return conn


def create_tables():

    conn = get_connection()
    c = conn.cursor()

    c.execute('')
