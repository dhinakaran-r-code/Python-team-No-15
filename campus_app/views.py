from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, LoginForm, BookingForm, RejectionForm, AdminBookingForm
from .models import UserRole, Booking, Resource, StudentProfile, StaffProfile, BookingStatus
from django.core.exceptions import ValidationError

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('student_dashboard')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')
def dashboard(request):
    user = request.user
    if user.role == UserRole.ADMIN:
        return redirect('admin_dashboard')
    elif user.role == UserRole.STAFF:
        return redirect('staff_dashboard')
    elif user.role == UserRole.STUDENT:
        return redirect('student_dashboard')
    else:
        return redirect('login') 

@login_required
def student_dashboard(request):
    if request.user.role != UserRole.STUDENT:
        return redirect('dashboard')
    bookings = Booking.objects.filter(user=request.user)
    resources = Resource.objects.filter(status='AVAILABLE') 
    return render(request, 'student_dashboard.html', {'bookings': bookings, 'resources': resources})

@login_required
def staff_dashboard(request):
    if request.user.role != UserRole.STAFF:
        return redirect('dashboard')
    
    try:
        staff_profile = request.user.staff_profile
        department = staff_profile.department
        # Get pending bookings for students in this department
        pending_bookings = Booking.objects.filter(
            user__student_profile__department=department,
            status='PENDING'
        )
        return render(request, 'staff_dashboard.html', {'pending_bookings': pending_bookings, 'department': department})
    except StaffProfile.DoesNotExist:
        messages.error(request, "Staff profile not found.")
        return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')
    
    # Analytics
    total_students = StudentProfile.objects.count()
    total_staff = StaffProfile.objects.count()
    total_resources = Resource.objects.count()
    pending_bookings = Booking.objects.filter(status='PENDING').count()
    staff_approved_bookings = Booking.objects.filter(status='STAFF_APPROVED')
    
    context = {
        'total_students': total_students,
        'total_staff': total_staff,
        'total_resources': total_resources,
        'pending_bookings': pending_bookings,
        'staff_approved_bookings': staff_approved_bookings
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def book_resource(request):
    if request.user.role != UserRole.STUDENT:
        messages.error(request, "Only students can book resources.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.status = 'PENDING'
            try:
                booking.full_clean() 
                booking.save()
                messages.success(request, "Booking requested successfully! Waiting for staff approval.")
                return redirect('student_dashboard')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = BookingForm()
    
    return render(request, 'book_resource.html', {'form': form})

@login_required
def approve_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    
    if request.user.role == UserRole.STAFF:
        # Staff Approval -> STAFF_APPROVED
        try:
            if booking.user.student_profile.department != request.user.staff_profile.department:
                messages.error(request, "Unauthorized.")
                return redirect('staff_dashboard')
            
            booking.status = 'STAFF_APPROVED' # Moving to next stage
            booking.save()
            messages.success(request, f"Booking approved. Forwarded to Admin.")
            return redirect('staff_dashboard')
        except:
             return redirect('dashboard')

    elif request.user.role == UserRole.ADMIN:
        # Admin Approval -> APPROVED (Final)
        booking.status = 'APPROVED'
        booking.save()
        messages.success(request, f"Booking finally approved.")
        return redirect('admin_dashboard')
    
    else:
        messages.error(request, "Unauthorized.")
        return redirect('dashboard')

@login_required
def reject_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    
    if request.method == 'POST':
        form = RejectionForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            booking.status = 'REJECTED'
            booking.rejection_reason = reason
            booking.save()
            messages.success(request, "Booking rejected with reason.")
            return redirect('dashboard')
    else:
        form = RejectionForm()

    return render(request, 'reject_booking.html', {'form': form, 'booking': booking})

from datetime import timedelta

@login_required
def admin_book_resource(request):
    if request.user.role != UserRole.ADMIN:
        messages.error(request, "Unauthorized.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AdminBookingForm(request.POST)
        if form.is_valid():
            resource = form.cleaned_data['resource']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            
            # Iterate through dates
            current_date = start_date
            success_count = 0
            fail_count = 0
            
            while current_date <= end_date:
                # Create booking for each day
                booking = Booking(
                    user=request.user,
                    resource=resource,
                    booking_date=current_date,
                    start_time=start_time,
                    end_time=end_time,
                    status='APPROVED' # Admin bookings are auto-approved
                )
                try:
                    booking.full_clean()
                    booking.save()
                    success_count += 1
                except ValidationError:
                    fail_count += 1
                
                current_date += timedelta(days=1)
            
            if success_count > 0:
                messages.success(request, f"Successfully created {success_count} bookings.")
            if fail_count > 0:
                messages.warning(request, f"Failed to create {fail_count} bookings due to conflicts/errors.")
                
            return redirect('admin_dashboard')
    else:
        form = AdminBookingForm()
    
    return render(request, 'admin_book_resource.html', {'form': form})
