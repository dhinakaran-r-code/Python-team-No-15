import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection

try:
    user_count = User.objects.count()
    print(f"Database connection successful.")
    print(f"User count: {user_count}")
    print(f"Database vendor: {connection.vendor}")
except Exception as e:
    print(f"Database connection failed: {e}")
