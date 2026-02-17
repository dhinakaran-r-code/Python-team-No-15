from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import User, StudentProfile, StaffProfile, Resource, Booking, Department
from .forms import LoginForm, StudentRegistrationForm, StaffCreationForm, ResourceForm, BookingForm, DepartmentForm

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            
            if user and user.status == 'ACTIVE':
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Account is inactive or credentials are invalid')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.role = 'STUDENT'
            user.save()
            
            StudentProfile.objects.create(
                user=user,
                department=form.cleaned_data['department'],
                year=form.cleaned_data['year']
            )
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif request.user.role == 'STAFF':
        return redirect('staff_dashboard')
    else:
        return redirect('student_dashboard')

@login_required
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return redirect('dashboard')
    
    profile = request.user.student_profile
    resources = Resource.objects.filter(status='AVAILABLE')
    bookings = Booking.objects.filter(user=request.user)
    
    context = {
        'profile': profile,
        'resources': resources,
        'bookings': bookings,
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def staff_dashboard(request):
    if request.user.role != 'STAFF':
        return redirect('dashboard')
    
    profile = request.user.staff_profile
    students = StudentProfile.objects.filter(department=profile.department)
    bookings = Booking.objects.filter(user__student_profile__department=profile.department)
    
    context = {
        'profile': profile,
        'students': students,
        'bookings': bookings,
    }
    return render(request, 'staff_dashboard.html', context)

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    stats = {
        'total_students': User.objects.filter(role='STUDENT').count(),
        'total_staff': User.objects.filter(role='STAFF').count(),
        'total_resources': Resource.objects.count(),
        'available_resources': Resource.objects.filter(status='AVAILABLE').count(),
        'pending_bookings': Booking.objects.filter(status='PENDING').count(),
        'approved_bookings': Booking.objects.filter(status='APPROVED').count(),
    }
    
    recent_bookings = Booking.objects.all()[:10]
    
    context = {
        'stats': stats,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def create_booking(request):
    if request.user.role != 'STUDENT' or request.user.status != 'ACTIVE':
        messages.error(request, 'Only active students can create bookings')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking request submitted successfully')
            return redirect('student_dashboard')
    else:
        form = BookingForm()
    
    return render(request, 'booking_form.html', {'form': form})

@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.user.role == 'ADMIN':
        booking.status = 'APPROVED'
        booking.save()
        messages.success(request, 'Booking approved')
    elif request.user.role == 'STAFF':
        if booking.user.student_profile.department == request.user.staff_profile.department:
            booking.status = 'APPROVED'
            booking.save()
            messages.success(request, 'Booking approved')
        else:
            messages.error(request, 'You can only approve bookings from your department')
    
    return redirect('dashboard')

@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.user.role == 'ADMIN':
        booking.status = 'REJECTED'
        booking.save()
        messages.success(request, 'Booking rejected')
    elif request.user.role == 'STAFF':
        if booking.user.student_profile.department == request.user.staff_profile.department:
            booking.status = 'REJECTED'
            booking.save()
            messages.success(request, 'Booking rejected')
        else:
            messages.error(request, 'You can only reject bookings from your department')
    
    return redirect('dashboard')

@login_required
def manage_resources(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    resources = Resource.objects.all()
    return render(request, 'resource_list.html', {'resources': resources})

@login_required
def create_resource(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource created successfully')
            return redirect('manage_resources')
    else:
        form = ResourceForm()
    
    return render(request, 'resource_form.html', {'form': form, 'action': 'Create'})

@login_required
def edit_resource(request, resource_id):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    resource = get_object_or_404(Resource, id=resource_id)
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource updated successfully')
            return redirect('manage_resources')
    else:
        form = ResourceForm(instance=resource)
    
    return render(request, 'resource_form.html', {'form': form, 'action': 'Edit'})

@login_required
def delete_resource(request, resource_id):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    resource = get_object_or_404(Resource, id=resource_id)
    resource.delete()
    messages.success(request, 'Resource deleted successfully')
    return redirect('manage_resources')

@login_required
def manage_departments(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

@login_required
def create_department(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully')
            return redirect('manage_departments')
    else:
        form = DepartmentForm()
    
    return render(request, 'department_form.html', {'form': form})

@login_required
def create_staff(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff created successfully')
            return redirect('admin_dashboard')
    else:
        form = StaffCreationForm()
    
    return render(request, 'staff_form.html', {'form': form})

@login_required
def manage_users(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    users = User.objects.all().exclude(role='ADMIN')
    return render(request, 'user_list.html', {'users': users})

@login_required
def toggle_user_status(request, user_id):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    user.status = 'INACTIVE' if user.status == 'ACTIVE' else 'ACTIVE'
    user.save()
    messages.success(request, f'User status updated to {user.status}')
    return redirect('manage_users')
