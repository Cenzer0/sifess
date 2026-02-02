import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sifess.settings')
django.setup()

from django.contrib.auth import get_user_model

def fix_slugs():
    User = get_user_model()
    users = User.objects.filter(slug__isnull=True)
    print(f"Found {users.count()} users with missing slugs.")
    
    for user in users:
        print(f"Fixing slug for: {user.username}")
        user.save() # Triggers the new save method which sets slug
        print(f" -> New slug: {user.slug}")
    
    # Also fix empty strings if any
    users_empty = User.objects.filter(slug='')
    print(f"Found {users_empty.count()} users with empty slugs.")
    for user in users_empty:
        print(f"Fixing empty slug for: {user.username}")
        user.slug = None # Reset to trigger generation
        user.save()
        print(f" -> New slug: {user.slug}")

    print("✅ Slug repair complete.")

if __name__ == '__main__':
    fix_slugs()
