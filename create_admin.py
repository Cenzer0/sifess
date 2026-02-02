import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sifess.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    username = 'admin'
    email = 'admin@example.com'
    password = 'password123'

    print(f"Checking for user: {username}...")
    
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}")
        try:
            # Create superuser
            User.objects.create_superuser(username, email, password)
            print(f"✅ Superuser '{username}' created successfully!")
            print(f"Password: {password}")
        except Exception as e:
            print(f"❌ Error creating superuser: {e}")
    else:
        print(f"ℹ️  Superuser '{username}' already exists.")

if __name__ == '__main__':
    create_superuser()
