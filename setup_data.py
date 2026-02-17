"""
Campus Resource Management System - Setup Script
Run this after configuring .env file
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_project.settings')
django.setup()

from campus_app.models import User, Department, Resource

def create_sample_data():
    print("Creating sample data for Campus Resource Management System\n")
    
    # Create Departments
    print("Creating Departments...")
    departments = [
        {'name': 'Computer Science Engineering', 'code': 'CSE'},
        {'name': 'Artificial Intelligence & ML', 'code': 'AIML'},
        {'name': 'Electronics & Communication', 'code': 'ECE'},
        {'name': 'Mechanical Engineering', 'code': 'MECH'},
        {'name': 'Civil Engineering', 'code': 'CIVIL'},
    ]
    
    for dept_data in departments:
        dept, created = Department.objects.get_or_create(
            code=dept_data['code'],
            defaults={'name': dept_data['name']}
        )
        if created:
            print(f"  + Created: {dept.name} ({dept.code})")
        else:
            print(f"  - Already exists: {dept.name}")
    
    # Create Resources
    print("\nCreating Resources...")
    resources = [
        {'name': 'Computer Lab 1', 'type': 'LAB', 'capacity': 60},
        {'name': 'Computer Lab 2', 'type': 'LAB', 'capacity': 50},
        {'name': 'Seminar Hall A', 'type': 'HALL', 'capacity': 200},
        {'name': 'Seminar Hall B', 'type': 'HALL', 'capacity': 150},
        {'name': 'Classroom 101', 'type': 'CLASSROOM', 'capacity': 40},
        {'name': 'Classroom 102', 'type': 'CLASSROOM', 'capacity': 40},
        {'name': 'Auditorium', 'type': 'HALL', 'capacity': 500},
    ]
    
    for res_data in resources:
        res, created = Resource.objects.get_or_create(
            name=res_data['name'],
            defaults={
                'type': res_data['type'],
                'capacity': res_data['capacity'],
                'status': 'AVAILABLE'
            }
        )
        if created:
            print(f"  + Created: {res.name} ({res.get_type_display()}, Capacity: {res.capacity})")
        else:
            print(f"  - Already exists: {res.name}")
    
    print("\nSample data created successfully!")
    print("\nNext Steps:")
    print("1. Create admin user: python manage.py createsuperuser")
    print("2. Set admin role in Django shell")
    print("3. Run server: python manage.py runserver")
    print("4. Access at: http://localhost:8000")

if __name__ == '__main__':
    try:
        create_sample_data()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have:")
        print("1. Configured .env file with database credentials")
        print("2. Run migrations: python manage.py migrate")
        sys.exit(1)
