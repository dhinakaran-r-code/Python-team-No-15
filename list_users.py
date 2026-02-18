import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_project.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def list_and_reset_users():
    print("-" * 60)
    print(f"{'Role':<15} | {'Username':<20} | {'Password':<15}")
    print("-" * 60)

    users = User.objects.all().order_by('role', 'username')
    
    for user in users:
        # Reset password to a known default for demonstration
        password = "password123" 
        user.set_password(password)
        user.save()
        
        role_name = user.role if hasattr(user, 'role') else 'Start'
        print(f"{role_name:<15} | {user.username:<20} | {password:<15}")

    print("-" * 60)
    print("\nAll passwords have been reset to 'password123'.")

if __name__ == "__main__":
    list_and_reset_users()
