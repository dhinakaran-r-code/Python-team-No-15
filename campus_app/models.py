from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# --- Constants & Choices ---

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', _('Admin')
    STAFF = 'STAFF', _('Staff')
    STUDENT = 'STUDENT', _('Student')

class ResourceType(models.TextChoices):
    LAB = 'LAB', _('Lab')
    CLASSROOM = 'CLASSROOM', _('Classroom')
    HALL = 'HALL', _('Event Hall')
    COMPUTER = 'COMPUTER', _('Computer')

class ResourceStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', _('Available')
    UNAVAILABLE = 'UNAVAILABLE', _('Unavailable')
    MAINTENANCE = 'MAINTENANCE', _('Maintenance')

class BookingStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    APPROVED = 'APPROVED', _('Approved')
    REJECTED = 'REJECTED', _('Rejected')

class Department(models.TextChoices):
    CSE = 'CSE', _('Computer Science')
    AIML = 'AIML', _('AI & ML')
    ECE = 'ECE', _('Electronics')
    MECH = 'MECH', _('Mechanical')
    CIVIL = 'CIVIL', _('Civil')
    # Add more as needed

# --- Models ---

class User(AbstractUser):
    role = models.CharField(
        max_length=10, 
        choices=UserRole.choices, 
        default=UserRole.STUDENT
    )
    phone = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = UserRole.ADMIN
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    @property
    def is_staff_member(self):
        return self.role == UserRole.STAFF
    
    @property
    def is_student(self):
        return self.role == UserRole.STUDENT


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    department = models.CharField(max_length=10, choices=Department.choices, unique=True) # One staff per department

    def __str__(self):
        return f"{self.user.username} - {self.department} Staff"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    department = models.CharField(max_length=10, choices=Department.choices)
    year = models.IntegerField(choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')])
    is_representative = models.BooleanField(default=False)

    def clean(self):
        # Validate one representative per department constraint validation logic
        if self.is_representative:
            existing_rep = StudentProfile.objects.filter(
                department=self.department, 
                is_representative=True
            ).exclude(pk=self.pk).exists()
            if existing_rep:
                raise ValidationError(f"A representative already exists for {self.department}.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.department} ({self.year})"


class Resource(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ResourceType.choices)
    capacity = models.IntegerField()
    status = models.CharField(
        max_length=20, 
        choices=ResourceStatus.choices, 
        default=ResourceStatus.AVAILABLE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('STAFF_APPROVED', 'Staff Approved'), # Approved by Staff, pending Admin
        ('APPROVED', 'Approved'),             # Final Approval by Admin
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    start_time = models.TimeField(help_text="Start time (09:00 - 16:00)", default='09:00')
    end_time = models.TimeField(help_text="End time (09:00 - 16:00)", default='17:00')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING'
    )
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        # Time Range Validation (9 AM - 4 PM)
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("End time must be after start time.")
            
            campus_start = timezone.datetime.strptime("09:00", "%H:%M").time()
            campus_end = timezone.datetime.strptime("16:00", "%H:%M").time()
            
            if self.start_time < campus_start or self.end_time > campus_end:
                 raise ValidationError("Bookings are only allowed between 9:00 AM and 4:00 PM.")

        # Overlap Validation
        # Check against APPROVED or STAFF_APPROVED bookings
        # (Status='REJECTED' or 'PENDING' usually shouldn't block? 
        # Actually PENDING might block to prevent race conditions, but for now let's say only APPROVED blocks?
        # Safe approach: Check against any non-REJECTED booking to prevent double booking attempts?
        # Let's block if there is an existing APPROVED or STAFF_APPROVED booking.)
        
        overlapping = Booking.objects.filter(
            resource=self.resource,
            booking_date=self.booking_date,
            status__in=['APPROVED', 'STAFF_APPROVED']
        ).exclude(pk=self.pk)

        # Overlap logic: (StartA < EndB) and (EndA > StartB)
        for booking in overlapping:
            if self.start_time < booking.end_time and self.end_time > booking.start_time:
                 raise ValidationError(f"Resource is already booked from {booking.start_time} to {booking.end_time}.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.resource.name} ({self.booking_date})"
