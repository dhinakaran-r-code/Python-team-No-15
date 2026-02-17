# MySQL Not Installed - Setup Instructions

## Option 1: Install MySQL (Recommended for Production)

### Download & Install MySQL:
1. Download from: https://dev.mysql.com/downloads/installer/
2. Run installer and select "MySQL Server"
3. Set root password during installation
4. Start MySQL service

### After Installation:
1. Update `.env` file with your MySQL password
2. Create database: Open MySQL Command Line Client
   ```sql
   CREATE DATABASE campus_db;
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```

---

## Option 2: Use SQLite (Quick Testing)

For quick testing without MySQL installation:

1. Update `campus_project/settings.py` database config:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

---

## Option 3: Use XAMPP (Easiest)

1. Download XAMPP: https://www.apachefriends.org/
2. Install and start MySQL from XAMPP Control Panel
3. MySQL runs without password by default
4. Keep `.env` password empty
5. Run migrations

---

**Current Status:** MySQL is not installed on your system.
**Recommendation:** Install XAMPP for easiest setup.
