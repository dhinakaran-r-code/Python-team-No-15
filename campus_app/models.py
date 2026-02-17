from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('STAFF', 'Staff'),
        ('STUDENT', 'Student'),
    ]
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    is_representative = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['department', 'is_representative']
        constraints = [
            models.UniqueConstraint(
                fields=['department'],
                condition=models.Q(is_representative=True),
                name='unique_representative_per_department'
            )
        ]
    
    def clean(self):
        if self.is_representative:
            existing = StudentProfile.objects.filter(
                department=self.department, 
                is_representative=True
            ).exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError('Department already has a representative')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department.code} Year {self.year}"

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    department = models.OneToOneField(Department, on_delete=models.CASCADE, related_name='staff')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department.name}"

class Resource(models.Model):
    TYPE_CHOICES = [
        ('LAB', 'Lab'),
        ('CLASSROOM', 'Classroom'),
        ('HALL', 'Event Hall'),
        ('COMPUTER', 'Computer'),
    ]
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('UNAVAILABLE', 'Unavailable'),
        ('MAINTENANCE', 'Maintenance'),
    ]
    
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.type})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    time_slot = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['resource', 'booking_date', 'time_slot']
        ordering = ['-created_at']
    
    def clean(self):
        if self.pk is None:
            existing = Booking.objects.filter(
                resource=self.resource,
                booking_date=self.booking_date,
                time_slot=self.time_slot
            ).exclude(status='REJECTED')
            if existing.exists():
                raise ValidationError('Resource already booked for this time slot')
    
    def __str__(self):
        return f"{self.resource.name} - {self.booking_date} {self.time_slot}"
