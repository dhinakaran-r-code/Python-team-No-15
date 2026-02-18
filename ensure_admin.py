import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_project.settings')
django.setup()

User = get_user_model()
try:
    user, created = User.objects.get_or_create(username='admin', defaults={
        'email': 'admin@campus.edu',
        'is_staff': True,
        'is_superuser': True
    })
    
    if created:
        user.set_password('admin123')
        user.role = 'ADMIN'
        user.save()
        print("Superuser 'admin' created with password 'admin123'.")
    else:
        print("Superuser 'admin' already exists. Resetting password and ensuring admin role.")
        user.email = 'admin@campus.edu'
        user.set_password('admin123')
        user.role = 'ADMIN'
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print("Superuser 'admin' updated.")

except Exception as e:
    print(f"Error creating superuser: {e}")
