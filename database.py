# database.py

import mysql.connector
from mysql.connector import Error

class Database:  # Make sure this class is defined
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='geccs_activity_system',  # Your database name
                user='root',
                password='',       # Your database password
                port=3306
            )
            return connection
        except Error as e:
            raise Exception(f"Database connection failed: {e}")