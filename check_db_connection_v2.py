import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()

try:
    print(f"Using User model: {User.__name__}")
    user_count = User.objects.count()
    print(f"Database connection successful.")
    print(f"User count: {user_count}")
    print(f"Database vendor: {connection.vendor}")
    
    # Also check if we can list table names
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Found {len(tables)} tables.")
        
except Exception as e:
    print(f"Database connection failed: {e}")
