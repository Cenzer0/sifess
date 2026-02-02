import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sifess.settings')
django.setup()

from confessions.tasks import send_daily_recap, cleanup_old_confessions

print("--- Running Cleanup Task ---")
# Calling directly (synchronously) since we are testing without a worker
result_cleanup = cleanup_old_confessions()
print(f"Result: {result_cleanup}")

print("\n--- Running Daily Recap Task ---")
result_recap = send_daily_recap()
print(f"Result: {result_recap}")

print("\n✅ Manual task execution complete.")
