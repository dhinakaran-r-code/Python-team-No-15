from django.urls import path
from . import api_views

urlpatterns = [
    # User Management APIs
    path('api/users/', api_views.get_all_users, name='api_get_users'),
    path('api/users/create/', api_views.create_user, name='api_create_user'),
    path('api/users/<int:user_id>/', api_views.get_user_by_id, name='api_get_user'),
    path('api/users/<int:user_id>/update/', api_views.update_user, name='api_update_user'),
    path('api/users/<int:user_id>/delete/', api_views.delete_user, name='api_delete_user'),
    
    # Resource Management APIs
    path('api/resources/', api_views.get_all_resources, name='api_get_resources'),
    path('api/resources/create/', api_views.create_resource, name='api_create_resource'),
    path('api/resources/<int:resource_id>/', api_views.get_resource_by_id, name='api_get_resource'),
    path('api/resources/<int:resource_id>/update/', api_views.update_resource, name='api_update_resource'),
    path('api/resources/<int:resource_id>/delete/', api_views.delete_resource, name='api_delete_resource'),
    
    # Booking Management APIs
    path('api/bookings/', api_views.get_all_bookings, name='api_get_bookings'),
    path('api/bookings/create/', api_views.create_booking, name='api_create_booking'),
    path('api/bookings/<int:booking_id>/', api_views.get_booking_by_id, name='api_get_booking'),
    path('api/bookings/<int:booking_id>/status/', api_views.update_booking_status, name='api_update_booking_status'),
    path('api/bookings/<int:booking_id>/delete/', api_views.delete_booking, name='api_delete_booking'),
]
