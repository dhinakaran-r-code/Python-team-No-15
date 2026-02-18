from django.urls import path
from .views import (
    register_student, user_login, user_logout, dashboard,
    student_dashboard, staff_dashboard, admin_dashboard,
    book_resource, staff_book_resource, approve_booking, approve_booking_rep, reject_booking, admin_book_resource,
    admin_resource_list, admin_booking_list,
    admin_add_resource, admin_add_staff, admin_add_student,
    admin_student_departments, admin_student_years, admin_student_list_by_year,
    admin_staff_departments, admin_staff_years, admin_staff_list_by_year
)

urlpatterns = [
    path('register/', register_student, name='register_student'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/student/', student_dashboard, name='student_dashboard'),
    path('dashboard/staff/', staff_dashboard, name='staff_dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('book/', book_resource, name='book_resource'),
    path('staff/book/', staff_book_resource, name='staff_book_resource'),
    path('approve/<int:booking_id>/', approve_booking, name='approve_booking'),
    path('approve_rep/<int:booking_id>/', approve_booking_rep, name='approve_booking_rep'),
    path('reject/<int:booking_id>/', reject_booking, name='reject_booking'),
    path('admin/book/', admin_book_resource, name='admin_book_resource'),
    path('admin/resources/', admin_resource_list, name='admin_resource_list'),
    
    # Student Hierarchy URLs
    path('admin/students/', admin_student_departments, name='admin_student_departments'),
    path('admin/students/<str:department_code>/', admin_student_years, name='admin_student_years'),
    path('admin/students/<str:department_code>/<int:year>/', admin_student_list_by_year, name='admin_student_list_by_year'),
    
    # Staff Hierarchy URLs
    path('admin/staff/', admin_staff_departments, name='admin_staff_departments'),
    path('admin/staff/<str:department_code>/', admin_staff_years, name='admin_staff_years'),
    path('admin/staff/<str:department_code>/<int:year>/', admin_staff_list_by_year, name='admin_staff_list_by_year'),
    
    path('admin/bookings/', admin_booking_list, name='admin_booking_list'),
    path('admin/resource/add/', admin_add_resource, name='admin_add_resource'),
    path('admin/staff/add/', admin_add_staff, name='admin_add_staff'),
    path('admin/student/add/', admin_add_student, name='admin_add_student'),
]
