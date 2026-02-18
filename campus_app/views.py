from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, LoginForm, BookingForm, RejectionForm, AdminBookingForm
from .models import UserRole, Booking, Resource, StudentProfile, StaffProfile, BookingStatus, User, Department
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
    
    # Get user's bookings
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    # If Class Rep, get requests from their class
    class_requests = None
    try:
        student_profile = request.user.student_profile
        if student_profile.is_representative:
            department = student_profile.department
            year = student_profile.year
            # Filter for PENDING_REP status in same Class
            class_requests = Booking.objects.filter(
                user__student_profile__department=department,
                user__student_profile__year=year,
                status='PENDING_REP'
            ).exclude(user=request.user) # Exclude own bookings
    except StudentProfile.DoesNotExist:
        pass

    return render(request, 'student_dashboard.html', {
        'bookings': bookings, 
        'class_requests': class_requests
    })

@login_required
def staff_dashboard(request):
    if request.user.role != UserRole.STAFF:
        return redirect('dashboard')
    
    try:
        staff_profile = request.user.staff_profile
        department = staff_profile.department
        year = staff_profile.year
        
        # Get pending bookings for specific Dept AND Year
        # Staff only sees bookings that have been approved by Rep (PENDING_STAFF)
        # OR if the student is a Rep/Staff themselves? 
        # Requirement: "rep approved and go to the relatedd year department staff"
        pending_bookings = Booking.objects.filter(
            user__student_profile__department=department,
            user__student_profile__year=year,
            status='PENDING_STAFF'
        )
        
        # Get booking history for specific Dept AND Year
        history_bookings = Booking.objects.filter(
            user__student_profile__department=department,
            user__student_profile__year=year
        ).exclude(status='PENDING').order_by('-created_at')

        return render(request, 'staff_dashboard.html', {
            'pending_bookings': pending_bookings, 
            'history_bookings': history_bookings,
            'department': department,
            'year': year
        })
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
    
    # Count of bookings waiting for Admin (STAFF_APPROVED)
    pending_bookings = Booking.objects.filter(status='STAFF_APPROVED').count()
    
    # List of bookings waiting for Admin
    staff_approved_bookings = Booking.objects.filter(status='STAFF_APPROVED').order_by('created_at')
    
    context = {
        'total_students': total_students,
        'total_staff': total_staff,
        'total_resources': total_resources,
        'pending_bookings': pending_bookings, # Count for card
        'staff_approved_bookings': staff_approved_bookings # List for table
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
            
            # Set initial status based on role
            if hasattr(request.user, 'student_profile') and request.user.student_profile.is_representative:
                booking.status = 'PENDING_STAFF' # Reps skip to Staff approval
                msg = "Booking requested! Sent to Faculty Advisor for approval."
            else:
                booking.status = 'PENDING_REP' # Students go to Rep first
                msg = "Booking requested! Sent to Class Representative for approval."
            
            try:
                booking.full_clean() 
                booking.save()
                messages.success(request, msg)
                return redirect('student_dashboard')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = BookingForm()
    
    return render(request, 'book_resource.html', {'form': form})

@login_required
def staff_book_resource(request):
    if request.user.role != UserRole.STAFF:
        messages.error(request, "Only staff can access this page.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            # Staff bookings are automatically approved by staff (themselves/colleagues) 
            # and go directly to Admin for final approval.
            booking.status = 'STAFF_APPROVED' 
            
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, "Booking request submitted! Forwarded to Admin for final approval.")
                return redirect('staff_dashboard')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = BookingForm()
    
    return render(request, 'staff_book_resource.html', {'form': form})

@login_required
def approve_booking_rep(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user is Rep and authorized
    try:
        rep_profile = request.user.student_profile
        if not rep_profile.is_representative:
            messages.error(request, "Unauthorized. Only Class Reps can perform this action.")
            return redirect('dashboard')
            
        if (booking.user.student_profile.department != rep_profile.department or 
            booking.user.student_profile.year != rep_profile.year):
            messages.error(request, "Unauthorized. You can only approve for your Class.")
            return redirect('dashboard')
            
        # Move to next stage: PENDING_STAFF
        booking.status = 'PENDING_STAFF' 
        booking.save()
        messages.success(request, "Booking approved! Forwarded to Faculty Advisor.")
        return redirect('student_dashboard')

    except Exception:
        return redirect('dashboard')

@login_required
def approve_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    
    if request.user.role == UserRole.STAFF:
        # Staff Approval -> STAFF_APPROVED
        try:
            if (booking.user.student_profile.department != request.user.staff_profile.department or
                booking.user.student_profile.year != request.user.staff_profile.year):
                messages.error(request, "Unauthorized. You can only approve for your Class.")
                return redirect('staff_dashboard')
            
            # Staff Approval -> STAFF_APPROVED (Pending Admin)
            booking.status = 'STAFF_APPROVED' 
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
    
    # Permission Check
    if request.user.role == UserRole.STAFF:
        try:
            if (booking.user.student_profile.department != request.user.staff_profile.department or
                booking.user.student_profile.year != request.user.staff_profile.year):
                messages.error(request, "Unauthorized. You can only reject for your Class.")
                return redirect('staff_dashboard')
        except:
            return redirect('dashboard')
    elif request.user.role != UserRole.ADMIN:
        messages.error(request, "Unauthorized.")
        return redirect('dashboard')
    
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
    
@login_required
def admin_booking_list(request):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')
    
    status_filter = request.GET.get('status', 'PENDING')
    bookings = Booking.objects.filter(status=status_filter).order_by('booking_date')
    
    return render(request, 'admin_booking_list.html', {
        'bookings': bookings, 
        'filter_status': status_filter
    })

@login_required
def admin_resource_list(request):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')
    
    resources = Resource.objects.all().order_by('name')
    return render(request, 'admin_resource_list.html', {'resources': resources})

@login_required
def admin_student_departments(request):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')
    
    # Get distinct departments from Department choices
    departments = Department.choices
    return render(request, 'admin_student_departments.html', {'departments': departments})

@login_required
def admin_student_years(request, department_code):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')
    
    # Verify department code is valid
    dept_label = dict(Department.choices).get(department_code)
    if not dept_label:
        messages.error(request, "Invalid Department")
        return redirect('admin_student_departments')

    return render(request, 'admin_student_years.html', {
        'department_code': department_code, 
        'department_label': dept_label,
        'years': [1, 2, 3, 4]
    })

@login_required
def admin_student_list_by_year(request, department_code, year):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')

    dept_label = dict(Department.choices).get(department_code)
    
    # Filter students
    students = User.objects.filter(
        role=UserRole.STUDENT,
        student_profile__department=department_code,
        student_profile__year=year
    ).select_related('student_profile').order_by('username')
    
    return render(request, 'admin_student_list.html', {
        'students': students,
        'department_code': department_code,
        'department_label': dept_label,
        'year': year
    })

@login_required
def admin_staff_departments(request):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')
    
    # Get distinct departments from Department choices
    departments = Department.choices
    return render(request, 'admin_staff_departments.html', {'departments': departments})

@login_required
def admin_staff_years(request, department_code):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')
    
    # Verify department code is valid
    dept_label = dict(Department.choices).get(department_code)
    if not dept_label:
        messages.error(request, "Invalid Department")
        return redirect('admin_staff_departments')

    return render(request, 'admin_staff_years.html', {
        'department_code': department_code, 
        'department_label': dept_label,
        'years': [1, 2, 3, 4]
    })

@login_required
def admin_staff_list_by_year(request, department_code, year):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')

    dept_label = dict(Department.choices).get(department_code)
    
    # Filter staff
    staff_members = User.objects.filter(
        role=UserRole.STAFF,
        staff_profile__department=department_code,
        staff_profile__year=year
    ).select_related('staff_profile').order_by('username')
    
    return render(request, 'admin_staff_list.html', {
        'staff_members': staff_members,
        'department_code': department_code,
        'department_label': dept_label,
        'year': year
    })

from .forms import ResourceForm, StaffRegistrationForm, StudentAddForm

@login_required
def admin_add_resource(request):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource added successfully.")
            return redirect('admin_resource_list')
    else:
        form = ResourceForm()
    
    return render(request, 'admin_add_resource.html', {'form': form})

@login_required
def admin_add_staff(request):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member added successfully.")
            return redirect('admin_staff_list')
    else:
        form = StaffRegistrationForm()
        
    return render(request, 'admin_add_staff.html', {'form': form})

@login_required
def admin_add_student(request):
    if request.user.role != UserRole.ADMIN:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully.")
            return redirect('admin_student_list')
    else:
        form = StudentAddForm()
        
    return render(request, 'admin_add_student.html', {'form': form})
