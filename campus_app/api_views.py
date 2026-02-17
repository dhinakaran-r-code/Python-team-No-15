from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import User, Resource, Booking
from .serializers import UserSerializer, ResourceSerializer, BookingSerializer

# ============ USER MANAGEMENT APIs ============

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data.get('password', 'password123'))
        user.username = user.email
        user.save()
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Validation failed'
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_users(request):
    status_filter = request.query_params.get('status', None)
    users = User.objects.all()
    
    if status_filter:
        users = users.filter(status=status_filter.upper())
    
    serializer = UserSerializer(users, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'message': 'Users retrieved successfully'
    })

@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'User retrieved successfully'
        })
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'User updated successfully'
            })
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Validation failed'
        }, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        # Soft delete
        user.status = 'INACTIVE'
        user.save()
        return Response({
            'success': True,
            'message': 'User deleted successfully (soft delete)'
        })
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)

# ============ RESOURCE MANAGEMENT APIs ============

@api_view(['POST'])
def create_resource(request):
    serializer = ResourceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Resource created successfully'
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Validation failed'
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_resources(request):
    resources = Resource.objects.all()
    serializer = ResourceSerializer(resources, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'message': 'Resources retrieved successfully'
    })

@api_view(['GET'])
def get_resource_by_id(request, resource_id):
    try:
        resource = Resource.objects.get(id=resource_id)
        serializer = ResourceSerializer(resource)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Resource retrieved successfully'
        })
    except Resource.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Resource not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
def update_resource(request, resource_id):
    try:
        resource = Resource.objects.get(id=resource_id)
        serializer = ResourceSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Resource updated successfully'
            })
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Validation failed'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Resource.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Resource not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_resource(request, resource_id):
    try:
        resource = Resource.objects.get(id=resource_id)
        resource.delete()
        return Response({
            'success': True,
            'message': 'Resource deleted successfully'
        })
    except Resource.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Resource not found'
        }, status=status.HTTP_404_NOT_FOUND)

# ============ BOOKING MANAGEMENT APIs ============

@api_view(['POST'])
@transaction.atomic
def create_booking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Booking created successfully'
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Validation failed'
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_bookings(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'message': 'Bookings retrieved successfully'
    })

@api_view(['GET'])
def get_booking_by_id(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        serializer = BookingSerializer(booking)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Booking retrieved successfully'
        })
    except Booking.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Booking not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def update_booking_status(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        new_status = request.data.get('status')
        
        if new_status not in ['PENDING', 'APPROVED', 'REJECTED']:
            return Response({
                'success': False,
                'message': 'Invalid status. Must be PENDING, APPROVED, or REJECTED'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = new_status
        booking.save()
        
        serializer = BookingSerializer(booking)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': f'Booking {new_status.lower()} successfully'
        })
    except Booking.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Booking not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
        return Response({
            'success': True,
            'message': 'Booking deleted successfully'
        })
    except Booking.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Booking not found'
        }, status=status.HTTP_404_NOT_FOUND)
