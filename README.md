# Campus Resource Management System

A Django-based system for managing campus resources, built for Hackathons.

## Features
- **User Roles**: Admin, Staff, Student.
- **Resource Management**: Labs, Classrooms, Halls (CRUD by Admin).
- **Booking System**: Student requests, Staff approvals, Double-booking prevention.
- **Dashboards**: Role-specific dashboards with status tracking.

## Prerequisites
- Python 3.8+
- PostgreSQL (Supabase) or SQLite (for local dev)

## Setup Instructions

1.  **Clone Requirements**
    ```bash
    git clone <repository_url>
    cd campus_project
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key
    # For Local Development (SQLite):
    DATABASE_URL=sqlite:///db.sqlite3
    # For Production (Supabase):
    # DATABASE_URL=postgres://user:password@host:port/dbname
    ```

5.  **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Create Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run Server**
    ```bash
    python manage.py runserver
    ```

## Usage Guide

### 1. Admin Setup
- Go to `http://127.0.0.1:8000/admin/`.
- Login with superuser credentials.
- Create **Resources** (e.g., "Computer Lab 1", "Seminar Hall").
- Create **Staff Users**:
    - Create a user with Staff status.
    - Create a **Staff Profile** for them linked to a department (e.g., CSE).

### 2. Student Registration
- Go to `http://127.0.0.1:8000/register/`.
- Register as a student (Select Department and Year).
- You will be redirected to the Student Dashboard.

### 3. Booking Flow
- **Student**: Click "Book New Resource", select resource and time.
- **Staff**: Login as staff of the same department. Approve/Reject the booking from the dashboard.
- **Student**: Check dashboard for status update (Approved/Rejected).

## Project Structure
- `campus_app/`: Core app logic (models, views, forms).
- `templates/`: HTML templates with Bootstrap 5.
- `static/`: Static assets.

## Deployment to Supabase
1.  Get your Connection String from Supabase Settings -> Database.
2.  Update `DATABASE_URL` in `.env`.
3.  Run `python manage.py migrate` database is empty.
4.  Deploys using standard Django deployment guides (Gunicorn/WhiteNoise included).
