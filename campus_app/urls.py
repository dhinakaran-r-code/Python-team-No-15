from django.urls import path
from .views import (
    register_student, user_login, user_logout, dashboard,
    student_dashboard, staff_dashboard, admin_dashboard,
    book_resource, approve_booking, reject_booking, admin_book_resource
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
    path('approve/<int:booking_id>/', approve_booking, name='approve_booking'),
    path('reject/<int:booking_id>/', reject_booking, name='reject_booking'),
    path('admin/book/', admin_book_resource, name='admin_book_resource'),
]
