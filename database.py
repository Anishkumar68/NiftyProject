import mysql.connector
from Config import Config


def get_connection():
    """Establish and return a database connection."""
    return mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
    )


def fetch_data(query, params=None):
    """Fetch data from MySQL using a query."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def insert_data(query, values):
    """Insert data into MySQL."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, values)
        conn.commit()
    except mysql.connector.IntegrityError:
        pass  # Skip duplicates
    finally:
        cursor.close()
        conn.close()
