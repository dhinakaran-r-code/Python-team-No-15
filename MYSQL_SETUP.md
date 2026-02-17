# 🎓 Campus Resource Management System - MySQL Setup

## MySQL Database Setup

### 1. Install MySQL
- Download from: https://dev.mysql.com/downloads/mysql/
- Or use XAMPP/WAMP (includes MySQL)

### 2. Create Database
```sql
-- Login to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE campus_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (optional)
CREATE USER 'campus_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON campus_db.* TO 'campus_user'@'localhost';
FLUSH PRIVILEGES;

-- Exit
EXIT;
```

### 3. Install MySQL Driver
```bash
pip install mysqlclient
```

**Windows Users:** If mysqlclient fails, use:
```bash
pip install pymysql
```
Then add to `campus_project/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 4. Configure .env
```env
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

### 6. Continue with Setup
Follow QUICKSTART.md from step 3 onwards.

---

## Troubleshooting

**Error: mysqlclient installation failed**
- Install Visual C++ Build Tools (Windows)
- Or use pymysql as alternative

**Error: Access denied for user**
- Check MySQL username/password
- Verify user has privileges on database

**Error: Can't connect to MySQL server**
- Ensure MySQL service is running
- Check host and port in .env

---

## Quick Test
```bash
# Test MySQL connection
mysql -u root -p -e "SHOW DATABASES;"
```
