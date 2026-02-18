# 🎓 Campus Resource Management System

A comprehensive, role-based web application for managing university resources (labs, halls, classrooms) with a multi-level approval workflow. Built with **Django 5**, **MySQL**, and **Bootstrap 5**.

---

## 🚀 Key Features

### 👥 User Roles & Hierarchy
*   **Admin**: Full system control, manages resources, users, and final approvals.
*   **Staff (Faculty Advisor)**: Approves student requests from their department/year and can book resources directly.
*   **Class Representative**: First line of approval for student requests within their class.
*   **Student**: Can request resources, view status, and see their class dashboard.

### 🔄 Intelligent Workflows
1.  **Student Booking**: Student Request → Class Rep Approval → Faculty Advisor Approval → Admin Final Approval.
2.  **Staff Booking**: Staff Request → Auto-approved at Dept Level → Admin Final Approval.
3.  **Admin Booking**: Instant global booking (rejects all conflicting requests).

### ⚡ Modern UI/UX
*   **Premium Dashboard Designs**: Glassmorphism effects, stat cards, and gradient themes.
*   **Dynamic status tracking**: Live status updates (Pending Rep, Pending Staff, Staff Approved, Approved).
*   **Responsive**: Fully functional on mobile and desktop.

---

## 🛠️ Technology Stack
*   **Backend**: Django 5.0 (Python)
*   **Database**: MySQL (Production-ready)
*   **Frontend**: HTML5, Bootstrap 5, Custom CSS
*   **Authentication**: Custom User Model with Role-Based Access Control (RBAC)

---

## ⚙️ Setup Instructions

### 1. Requirements
*   Python 3.10+
*   MySQL Server

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd campus_project

# Create Virtual Environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install Dependencies
pip install -r requirements.txt
```

### 3. Database Configuration
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secure-secret-key-here
# Update with your MySQL credentials:
DATABASE_URL=mysql://root:YourPassword@localhost:3306/campus_db
```

### 4. Database Setup
```bash
# Create Database (in MySQL Shell)
CREATE DATABASE campus_db;

# Run Migrations
python manage.py migrate

# Create Superuser (Admin)
python manage.py createsuperuser
```

### 5. Run the Application
```bash
python manage.py runserver
```
Access the site at: `http://127.0.0.1:8000/`

---

## 📖 Usage Guide

### 👨‍💼 Admin
*   **Login**: Use the superuser account.
*   **Dashboard**:
    *   **Manage Resources**: Add Labs, Seminar Halls, Classrooms.
    *   **Manage Users**: Add Staff and Students directly without admin panel.
    *   **Approvals**: Review "Needs Final Approval" cards and Approve/Reject bookings.
    *   **Bulk Booking**: Book a resource for multiple days at once.

### 🧑‍🏫 Staff (Faculty Advisor)
*   **Login**: Credentials provided by Admin.
*   **Dashboard**:
    *   **Approve Requests**: View and approve bookings from your department's students (after Rep approval).
    *   **Book Resource**: Directly book a lab for your classes (skips Rep approval).

### 👨‍🎓 Student & Class Rep
*   **Login**: Register or use provided credentials.
*   **Dashboard**:
    *   **Book Resource**: Request a venue for an event.
    *   **Class Rep Tasks**: If you are a Rep, you will see a "Class Requests" section to approve your classmates' bookings first.

---

## 📂 Project Structure
```
campus_project/
├── campus_app/           # Core Application Logic
│   ├── models.py         # Database Schema (User, Booking, Resource)
│   ├── views.py          # Business Logic & Controllers
│   ├── urls.py           # Route Definitions
│   └── forms.py          # Form Validations
├── templates/            # HTML Templates (Dashboards, Forms)
├── static/               # CSS, JS, and Images
├── campus_project/       # Project Settings
├── requirements.txt      # Python Dependencies
└── manage.py             # Django CLI
```

---

## 🤝 Contributing
1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

**Developed for Campus Resource Management** 🚀
