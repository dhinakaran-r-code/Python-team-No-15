from django.core.management.base import BaseCommand
from django.utils import timezone
from campus_app.models import User, UserRole, StudentProfile, StaffProfile, Resource, ResourceType, ResourceStatus, Department

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@campus.com', 'adminpass')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin/adminpass'))

        # Create Staff (CSE)
        if not User.objects.filter(username='staff_cse').exists():
            user = User.objects.create_user('staff_cse', 'staff_cse@campus.com', 'staffpass')
            user.role = UserRole.STAFF
            user.save()
            StaffProfile.objects.create(user=user, department=Department.CSE)
            self.stdout.write(self.style.SUCCESS('Created staff: staff_cse/staffpass (CSE)'))

        # Create Student (CSE)
        if not User.objects.filter(username='student_cse').exists():
            user = User.objects.create_user('student_cse', 'student_cse@campus.com', 'studentpass')
            user.role = UserRole.STUDENT
            user.save()
            StudentProfile.objects.create(user=user, department=Department.CSE, year=3, is_representative=True)
            self.stdout.write(self.style.SUCCESS('Created student: student_cse/studentpass (CSE, 3rd Year, Rep)'))

        # Create Resources
        resources = [
            {'name': 'Computer Lab 1', 'type': ResourceType.LAB, 'capacity': 30},
            {'name': 'Seminar Hall A', 'type': ResourceType.HALL, 'capacity': 100},
            {'name': 'Classroom 101', 'type': ResourceType.CLASSROOM, 'capacity': 60},
        ]

        for res_data in resources:
            if not Resource.objects.filter(name=res_data['name']).exists():
                Resource.objects.create(**res_data)
                self.stdout.write(self.style.SUCCESS(f"Created resource: {res_data['name']}"))

        self.stdout.write(self.style.SUCCESS('Data seeding completed.'))
