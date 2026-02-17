from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, StaffProfile, Resource, Booking

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone')}),
    )

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'year', 'is_representative')
    list_filter = ('department', 'year', 'is_representative')
    search_fields = ('user__username', 'user__email')

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    list_filter = ('department',)

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'capacity', 'status')
    list_filter = ('type', 'status')
    search_fields = ('name',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'booking_date', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'resource__name')
    # Admin can change status directly if needed

admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Booking, BookingAdmin)
