from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Confession
from notifications.models import Notification

@receiver(post_save, sender=Confession)
def create_confession_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.recipient,
            type='new_confession',
            title='New Secret Message! 🫣',
            message='Someone just confessed to you. Click to see what they said!',
            link='/u/dashboard/' # Or specific link if we had a detail view
        )
