# Campus Resource Management System - REST API

## Backend Challenge - 2026 Batch

A production-quality REST API backend for managing campus resources, users, and bookings.

---

## Tech Stack

- **Framework:** Django 5.0.1
- **API:** Django REST Framework 3.14.0
- **Database:** SQLite (MySQL ready)
- **ORM:** Django ORM

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Sample Data (Optional)
```bash
python setup_data.py
```

### 4. Start Server
```bash
python manage.py runserver
```

Server runs at: **http://localhost:8000**

---

## API Documentation

### Base URL
```
http://localhost:8000/api
```

### Response Format
All APIs return JSON in this format:
```json
{
  "success": true,
  "data": {...},
  "message": "Readable message"
}
```

---

## MODULE 1: User Management APIs

### 1. Create User
**POST** `/api/users/create/`

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "role": "STUDENT",
  "password": "password123"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "role": "STUDENT",
    "status": "ACTIVE",
    "created_at": "2024-01-01T10:00:00Z"
  },
  "message": "User created successfully"
}
```

### 2. Get All Users
**GET** `/api/users/`

**Query Parameters:**
- `status` (optional): Filter by ACTIVE or INACTIVE

**Example:** `/api/users/?status=ACTIVE`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "phone": "1234567890",
      "role": "STUDENT",
      "status": "ACTIVE",
      "created_at": "2024-01-01T10:00:00Z"
    }
  ],
  "message": "Users retrieved successfully"
}
```

### 3. Get User by ID
**GET** `/api/users/{user_id}/`

**Response:** `200 OK`

### 4. Update User
**PUT/PATCH** `/api/users/{user_id}/update/`

**Request Body:**
```json
{
  "phone": "9876543210",
  "status": "INACTIVE"
}
```

**Response:** `200 OK`

### 5. Delete User (Soft Delete)
**DELETE** `/api/users/{user_id}/delete/`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "User deleted successfully (soft delete)"
}
```

---

## MODULE 2: Resource Management APIs

### 1. Create Resource
**POST** `/api/resources/create/`

**Request Body:**
```json
{
  "name": "Computer Lab 1",
  "type": "LAB",
  "capacity": 60,
  "status": "AVAILABLE"
}
```

**Valid Types:** `LAB`, `CLASSROOM`, `HALL`, `COMPUTER`

**Response:** `201 Created`

### 2. Get All Resources
**GET** `/api/resources/`

**Response:** `200 OK`

### 3. Get Resource by ID
**GET** `/api/resources/{resource_id}/`

**Response:** `200 OK`

### 4. Update Resource
**PUT/PATCH** `/api/resources/{resource_id}/update/`

**Request Body:**
```json
{
  "status": "UNAVAILABLE"
}
```

**Response:** `200 OK`

### 5. Delete Resource
**DELETE** `/api/resources/{resource_id}/delete/`

**Response:** `200 OK`

---

## MODULE 3: Booking Management APIs

### 1. Create Booking
**POST** `/api/bookings/create/`

**Request Body:**
```json
{
  "user": 1,
  "resource": 1,
  "booking_date": "2024-12-25",
  "time_slot": "09:00-10:00"
}
```

**Business Rules:**
- Resource must be AVAILABLE
- No double booking (same resource, date, time_slot)
- Default status: PENDING

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user": 1,
    "user_name": "John Doe",
    "resource": 1,
    "resource_name": "Computer Lab 1",
    "booking_date": "2024-12-25",
    "time_slot": "09:00-10:00",
    "status": "PENDING",
    "created_at": "2024-01-01T10:00:00Z"
  },
  "message": "Booking created successfully"
}
```

**Error (Double Booking):** `400 Bad Request`
```json
{
  "success": false,
  "errors": {
    "non_field_errors": ["Resource already booked for this time slot"]
  },
  "message": "Validation failed"
}
```

### 2. Get All Bookings
**GET** `/api/bookings/`

**Response:** `200 OK`

### 3. Get Booking by ID
**GET** `/api/bookings/{booking_id}/`

**Response:** `200 OK`

### 4. Update Booking Status
**PATCH** `/api/bookings/{booking_id}/status/`

**Request Body:**
```json
{
  "status": "APPROVED"
}
```

**Valid Status:** `PENDING`, `APPROVED`, `REJECTED`

**Response:** `200 OK`

### 5. Delete Booking
**DELETE** `/api/bookings/{booking_id}/delete/`

**Response:** `200 OK`

---

## Error Handling

### 404 Not Found
```json
{
  "success": false,
  "message": "User not found"
}
```

### 400 Bad Request
```json
{
  "success": false,
  "errors": {
    "email": ["Email already exists"],
    "capacity": ["Capacity must be positive"]
  },
  "message": "Validation failed"
}
```

---

## Testing with Postman

### Import Collection
1. Open Postman
2. Import → Link → Paste GitHub raw URL of `postman_collection.json`
3. Test all endpoints

### Test Double Booking
1. Create a booking: POST `/api/bookings/create/`
2. Try creating same booking again
3. Should return 400 error

---

## Database Schema

### User Model
- id (PK)
- first_name
- last_name
- email (unique)
- phone
- role (STUDENT/STAFF)
- status (ACTIVE/INACTIVE)
- created_at

### Resource Model
- id (PK)
- name
- type (LAB/CLASSROOM/HALL/COMPUTER)
- capacity (positive integer)
- status (AVAILABLE/UNAVAILABLE)
- created_at

### Booking Model
- id (PK)
- user (FK → User)
- resource (FK → Resource)
- booking_date
- time_slot
- status (PENDING/APPROVED/REJECTED)
- created_at
- **Constraint:** Unique (resource, booking_date, time_slot)

---

## Project Structure

```
campus_project/
├── campus_app/
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── api_views.py       # API view functions
│   ├── api_urls.py        # API URL routing
│   └── admin.py           # Admin configuration
├── campus_project/
│   ├── settings.py        # Django settings
│   └── urls.py            # Main URL config
├── requirements.txt       # Dependencies
├── manage.py              # Django CLI
└── README.md              # This file
```

---

## Key Features

✅ **CRUD Operations** - Complete Create, Read, Update, Delete for all modules  
✅ **Input Validation** - Server-side validation using DRF serializers  
✅ **Business Rules** - Double-booking prevention enforced  
✅ **Error Handling** - Clear error messages with proper HTTP codes  
✅ **REST Compliant** - Proper HTTP verbs and status codes  
✅ **Clean Code** - Modular, DRY principles, readable  
✅ **Database Integrity** - Foreign keys, constraints, migrations  

---

## Evaluation Checklist

- [x] User CRUD APIs
- [x] Resource CRUD APIs
- [x] Booking CRUD APIs
- [x] Filter users by status
- [x] Double-booking prevention
- [x] Input validation
- [x] Error handling
- [x] Clean JSON responses
- [x] Proper HTTP status codes
- [x] Database migrations
- [x] README documentation
- [x] Postman collection

---

## GitHub Repository

**URL:** https://github.com/dhinakaran-r-code/Python-team-15

---

## Contact

For questions or issues, refer to Django and DRF documentation:
- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)

---

**Ready for Backend Challenge Evaluation! 🚀**
