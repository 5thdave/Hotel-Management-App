import sqlite3

DB_NAME = "Hotel Management System.db"

def get_connection():
    return sqlite3.connect(DB_NAME)