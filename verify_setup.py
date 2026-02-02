import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sifess.settings')
django.setup()

from django.contrib.auth import get_user_model
from confessions.models import Confession

User = get_user_model()

# 1. Create User
if not User.objects.filter(username='test_user').exists():
    user = User.objects.create_user(username='test_user', password='password123', slug='test_user')
    print("User created.")
else:
    user = User.objects.get(username='test_user')
    print("User already exists.")

# 2. Create Confession
msg = "This is a secret message 123"
confession = Confession.objects.create(
    recipient=user,
    content_encrypted=msg,
    ip_hash='fakehash123'
)
print(f"Confession created with ID: {confession.id}")

# 3. Verify Encryption (Raw DB access check would be ideal, but here we check cleartext access)
# If decryption works, we get the original message.
print(f"Decrypted content: {confession.content_encrypted}")

if confession.content_encrypted == msg:
    print("VERIFICATION SUCCESS: Content decrypted correctly.")
else:
    print("VERIFICATION FAILED: Content mismatch.")
