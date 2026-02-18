import MySQLdb
import os
from dotenv import load_dotenv
import re

load_dotenv()

# Parse DATABASE_URL from .env
# Format: mysql://user:password@host:port/dbname
db_url = os.getenv('DATABASE_URL')
user = 'root'
password = ''
host = 'localhost'
port = 3306
dbname = 'campus_db'

if db_url and db_url.startswith('mysql://'):
    match = re.match(r'mysql://(.*?):(.*?)@(.*?):(\d+)/(.*)', db_url)
    if match:
        user, password, host, port, dbname = match.groups()

print(f"Connecting to MySQL at {host}:{port} as {user}...")

try:
    db = MySQLdb.connect(host=host, user=user, passwd=password, port=int(port))
    cursor = db.cursor()
    
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
    print(f"Database '{dbname}' created or already exists.")
    
    db.close()

except Exception as e:
    print(f"Error creating database: {e}")
    if "Access denied" in str(e):
        print("Please check your MySQL username and password in .env")
    elif "Can't connect" in str(e):
        print("Please ensure MySQL server is running.")
