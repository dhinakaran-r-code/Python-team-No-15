import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from campus_app.models import StudentProfile, StaffProfile

User = get_user_model()

DEPARTMENTS = ['CSE', 'ECE', 'MECH', 'CIVIL', 'IT']
YEARS = [1, 2, 3, 4]

def create_users():
    print("Populating Users (Staff, Representatives, Students)...")
    
    for dept in DEPARTMENTS:
        for year in YEARS:
            print(f"\nProcessing {dept} - Year {year}...")
            
            # 1. Create Staff Advisor for this Dept/Year
            staff_username = f"{year}{dept.lower()}_staff"
            staff_email = f"{staff_username}@campus.edu"
            staff_user, created = User.objects.get_or_create(username=staff_username, defaults={'email': staff_email})
            if created:
                staff_user.set_password('password123')
                staff_user.role = 'STAFF'
                staff_user.first_name = f"Staff ({dept})"
                staff_user.last_name = f"Year {year}"
                staff_user.save()
                StaffProfile.objects.create(user=staff_user, department=dept, year=year)
                print(f"  + Created Staff: {staff_username}")
            
            # 2. Create Class Representative
            rep_username = f"{year}{dept.lower()}_rep"
            rep_email = f"{rep_username}@campus.edu"
            rep_user, created = User.objects.get_or_create(username=rep_username, defaults={'email': rep_email})
            if created:
                rep_user.set_password('password123')
                rep_user.role = 'STUDENT'
                rep_user.first_name = f"Rep ({dept})"
                rep_user.last_name = f"Year {year}"
                rep_user.save()
                StudentProfile.objects.create(user=rep_user, department=dept, year=year, is_representative=True)
                print(f"  + Created Rep: {rep_username}")

            # 3. Create Regular Students (5 per class for now)
            for i in range(1, 6):
                stud_username = f"{year}{dept.lower()}_student_{i}"
                stud_email = f"{stud_username}@campus.edu"
                stud_user, created = User.objects.get_or_create(username=stud_username, defaults={'email': stud_email})
                if created:
                    stud_user.set_password('password123')
                    stud_user.role = 'STUDENT'
                    stud_user.first_name = f"Student {i}"
                    stud_user.last_name = f"({dept} {year})"
                    stud_user.save()
                    StudentProfile.objects.create(user=stud_user, department=dept, year=year, is_representative=False)
                    print(f"  + Created Student: {stud_username}")

    print("\nPopulation Complete!")

if __name__ == '__main__':
    try:
        create_users()
    except Exception as e:
        print(f"Error: {e}")
