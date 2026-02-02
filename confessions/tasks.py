from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import Confession
from notifications.models import Notification

User = get_user_model()

@shared_task
def send_daily_recap():
    """
    Sends a notification to users who received confessions in the last 24 hours.
    """
    now = timezone.now()
    yesterday = now - timedelta(days=1)
    
    # Get users who received confessions
    users = User.objects.filter(received_confessions__created_at__gte=yesterday).distinct()
    
    for user in users:
        count = user.received_confessions.filter(created_at__gte=yesterday).count()
        if count > 0:
            Notification.objects.create(
                recipient=user,
                type='daily_recap',
                title='Daily Recap 📅',
                message=f"You received {count} new confessions today! Check them out.",
                link='/dashboard/'
            )
    return f"Sent recaps to {users.count()} users."

@shared_task
def cleanup_old_confessions():
    """
    Deletes confessions older than 90 days to save space.
    """
    cutoff = timezone.now() - timedelta(days=90)
    deleted_count, _ = Confession.objects.filter(created_at__lte=cutoff).delete()
    return f"Deleted {deleted_count} old confessions."
