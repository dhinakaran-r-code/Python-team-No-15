from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Student
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('booking/create/', views.create_booking, name='create_booking'),
    
    # Staff
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('booking/<int:booking_id>/approve/', views.approve_booking, name='approve_booking'),
    path('booking/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
    
    # Admin
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('resources/', views.manage_resources, name='manage_resources'),
    path('resources/create/', views.create_resource, name='create_resource'),
    path('resources/<int:resource_id>/edit/', views.edit_resource, name='edit_resource'),
    path('resources/<int:resource_id>/delete/', views.delete_resource, name='delete_resource'),
    path('departments/', views.manage_departments, name='manage_departments'),
    path('departments/create/', views.create_department, name='create_department'),
    path('staff/create/', views.create_staff, name='create_staff'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),
]
