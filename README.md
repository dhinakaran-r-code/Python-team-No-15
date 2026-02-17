# 🎓 Campus Resource Management System

A comprehensive Django-based web application for managing campus resources, bookings, and user roles in an educational institution.

## 🚀 Features

### User Roles
- **Admin**: Complete system control, analytics, user management
- **Staff**: Department-specific student and booking management
- **Student**: Resource viewing and booking requests

### Core Modules
1. **User Management**: Role-based authentication and profiles
2. **Resource Management**: CRUD operations for campus resources
3. **Booking System**: Request, approve/reject bookings with conflict prevention
4. **Department Management**: Organize users by departments

### Key Highlights
- ✅ Prevents double-booking of resources
- ✅ One staff per department constraint
- ✅ One representative per department
- ✅ Role-based dashboards
- ✅ Modern, responsive UI
- ✅ MySQL database integration

---

## 📋 Prerequisites

- Python 3.8+
- MySQL Server 5.7+ or 8.0+
- pip (Python package manager)

---

## 🛠️ Installation & Setup

### 1. Clone or Download Project
```bash
cd campus_resource_management
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. MySQL Database Setup

#### Install MySQL
1. Download from [mysql.com](https://dev.mysql.com/downloads/mysql/)
2. Or use XAMPP/WAMP (includes MySQL)
3. Start MySQL service

#### Create Database
```sql
mysql -u root -p

CREATE DATABASE campus_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 4. Environment Configuration

Create `.env` file in project root:
```bash
cp .env.example .env
```

Edit `.env` with your MySQL credentials:
```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=campus_db
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

Follow prompts:
- Email: admin@campus.edu
- Username: admin
- Password: (your choice)

After creation, update role in Django shell:
```bash
python manage.py shell
```
```python
from campus_app.models import User
admin = User.objects.get(email='admin@campus.edu')
admin.role = 'ADMIN'
admin.save()
exit()
```

### 7. Load Sample Data (Optional)

Create departments via Django shell:
```bash
python manage.py shell
```
```python
from campus_app.models import Department

Department.objects.create(name='Computer Science Engineering', code='CSE')
Department.objects.create(name='Artificial Intelligence & ML', code='AIML')
Department.objects.create(name='Electronics & Communication', code='ECE')
Department.objects.create(name='Mechanical Engineering', code='MECH')
exit()
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Access at: **http://localhost:8000**

---

## 👥 User Workflows

### Admin Workflow
1. Login with superuser credentials
2. Create departments (if not done)
3. Add staff members (one per department)
4. Create resources (labs, classrooms, halls)
5. Monitor bookings and approve/reject
6. Manage user status (activate/deactivate)

### Staff Workflow
1. Register or get credentials from admin
2. Login → Staff Dashboard
3. View department students
4. Approve/reject booking requests from department students
5. Cannot access other departments

### Student Workflow
1. Register with department and year
2. Login → Student Dashboard
3. View available resources
4. Create booking requests
5. Track booking status (Pending/Approved/Rejected)

---

## 📁 Project Structure

```
campus_project/
│
├── campus_app/
│   ├── models.py          # Database models
│   ├── views.py           # Business logic
│   ├── forms.py           # Form validation
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin panel config
│   └── migrations/        # Database migrations
│
├── templates/
│   ├── base.html          # Base template
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── staff_dashboard.html
│   ├── admin_dashboard.html
│   ├── resource_list.html
│   ├── booking_form.html
│   └── ...
│
├── static/
│   ├── css/
│   └── js/
│
├── campus_project/
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL config
│   └── wsgi.py
│
├── .env                   # Environment variables (create this)
├── .env.example           # Environment template
├── requirements.txt       # Python dependencies
├── manage.py              # Django management
└── README.md
```

---

## 🔒 Security Features

- Password hashing (Django built-in)
- CSRF protection
- Role-based access control
- Environment variable configuration
- SQL injection prevention (Django ORM)
- Inactive user login prevention

---

## 🎨 UI/UX Features

- Modern gradient design
- Card-based layouts
- Status badges (color-coded)
- Responsive design
- Hover effects
- Empty state handling
- Django messages framework

---

## 🧪 Testing the System

### Test Scenario 1: Student Booking
1. Register as student
2. Create booking for available resource
3. Check status = PENDING
4. Login as staff (same department)
5. Approve booking
6. Login as student → status = APPROVED

### Test Scenario 2: Double Booking Prevention
1. Create booking for Resource A, Date X, Time Y
2. Try creating another booking for same resource/date/time
3. Should show error: "Resource already booked"

### Test Scenario 3: Department Isolation
1. Login as Staff (CSE department)
2. Try to approve booking from AIML student
3. Should not see AIML bookings

---

## 🚀 Deployment (Production)

### Environment Variables
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECRET_KEY=generate-strong-secret-key
```

### Static Files
```bash
python manage.py collectstatic
```

### Database
- Ensure MySQL is running
- Use proper connection pooling for production

### Hosting Options
- **Heroku**: Easy Django deployment
- **Railway**: Modern platform with PostgreSQL
- **PythonAnywhere**: Simple hosting
- **AWS/GCP**: Scalable cloud hosting

---

## 📊 Database Schema

### Models
- **User**: Extended Django user with role/status
- **Department**: Academic departments
- **StudentProfile**: Student-specific data
- **StaffProfile**: Staff-department mapping
- **Resource**: Campus resources
- **Booking**: Resource booking requests

### Key Constraints
- Unique email per user
- One staff per department
- One representative per department
- Unique booking per resource/date/time

---

## 🐛 Troubleshooting

### Database Connection Error
- Verify MySQL credentials in `.env`
- Check if MySQL service is running
- Ensure database `campus_db` exists

### Migration Errors
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear
```

### Admin Can't Login
Ensure role is set to 'ADMIN' in database

---

## 📝 Future Enhancements

- Email notifications for booking status
- Calendar view for bookings
- Resource availability dashboard
- Export reports (PDF/Excel)
- Mobile app integration
- Real-time notifications
- Booking history analytics

---

## 👨‍💻 Development Team

Built for college hackathon/project demonstration.

---

## 📄 License

Educational project - Free to use and modify.

---

## 🎯 Evaluation Points Covered

✅ CRUD Operations  
✅ Database Modeling  
✅ Authentication & Authorization  
✅ Business Logic Validation  
✅ Modern UI/UX  
✅ Role-Based Access Control  
✅ Production-Ready Structure  
✅ Documentation  
✅ Deployment Readiness  

---

## 📞 Support

For issues or questions, refer to Django documentation:
- [Django Docs](https://docs.djangoproject.com/)
- [MySQL Docs](https://dev.mysql.com/doc/)

---

**🚀 Ready for Hackathon Presentation!**
