# 🚀 QUICK START GUIDE

## Step-by-Step Setup (5 Minutes)

### 1. Configure Database
```bash
# Create MySQL database
mysql -u root -p -e "CREATE DATABASE campus_db;"

# Copy environment template
cp .env.example .env

# Edit .env with your MySQL credentials
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
# Email: admin@campus.edu
# Username: admin
# Password: admin123 (or your choice)
```

### 4. Set Admin Role
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

### 5. Load Sample Data
```bash
python setup_data.py
```

### 6. Run Server
```bash
python manage.py runserver
```

### 7. Access Application
Open browser: **http://localhost:8000**

---

## 🎯 Test Accounts

### Admin
- Email: admin@campus.edu
- Password: (what you set)
- Access: Full system control

### Create Staff (via Admin Dashboard)
1. Login as admin
2. Go to "Add Staff"
3. Assign to department

### Create Student (via Registration)
1. Go to /register
2. Fill form with department
3. Login and test booking

---

## 📋 Demo Checklist

- [ ] Admin can create departments
- [ ] Admin can create staff (one per department)
- [ ] Admin can create resources
- [ ] Student can register
- [ ] Student can create booking
- [ ] Staff can approve/reject bookings
- [ ] Double booking is prevented
- [ ] Role-based dashboards work
- [ ] User status toggle works

---

## 🐛 Common Issues

**Database Connection Error**
- Check .env file has correct MySQL credentials
- Verify MySQL service is running
- Ensure database exists: `mysql -u root -p -e "SHOW DATABASES;"`

**Admin Can't Access Dashboard**
- Ensure role is set to 'ADMIN' in step 4

**Migrations Error**
- Delete db.sqlite3 if exists
- Run migrations again

---

## 🎓 Presentation Tips

1. **Start with Admin Dashboard** - Show analytics
2. **Create a Resource** - Demonstrate CRUD
3. **Add Staff Member** - Show department constraint
4. **Register as Student** - Show user flow
5. **Create Booking** - Show validation
6. **Approve as Staff** - Show role-based access
7. **Try Double Booking** - Show prevention logic

---

**Ready to Present! 🚀**
