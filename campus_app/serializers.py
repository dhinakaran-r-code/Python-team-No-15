from rest_framework import serializers
from .models import User, Department, Resource, Booking, StudentProfile, StaffProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'role', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'created_at']
        read_only_fields = ['id', 'created_at']

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'type', 'capacity', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Capacity must be positive")
        return value

class BookingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'user_name', 'resource', 'resource_name', 'booking_date', 'time_slot', 'status', 'created_at']
        read_only_fields = ['id', 'created_at', 'user_name', 'resource_name']
    
    def validate(self, data):
        # Check resource availability
        resource = data.get('resource')
        if resource and resource.status != 'AVAILABLE':
            raise serializers.ValidationError("Resource is not available")
        
        # Check double booking
        booking_date = data.get('booking_date')
        time_slot = data.get('time_slot')
        
        if resource and booking_date and time_slot:
            existing = Booking.objects.filter(
                resource=resource,
                booking_date=booking_date,
                time_slot=time_slot
            ).exclude(status='REJECTED')
            
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise serializers.ValidationError("Resource already booked for this time slot")
        
        return data
