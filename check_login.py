import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sifess.settings')
django.setup()

import sys
print("Checking login...")
sys.stdout.flush()
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()
try:
    u = User.objects.get(username='admin')
    print(f"Found user: {u.username}, isActive: {u.is_active}, isStaff: {u.is_staff}, check_password: {u.check_password('password123')}")
except User.DoesNotExist:
    print("User admin does not exist")

user = authenticate(username='admin', password='password123')
if user:
    print("LOGIN SUCCESS: Admin credentials valid.")
else:
    print("LOGIN FAILED: Invalid credentials.")
