from django.db import models
from django.conf import settings
from core.fields import EncryptedTextField
from django.utils.translation import gettext_lazy as _
import uuid

class Confession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_confessions')
    
    # Encrypted content for privacy
    content_encrypted = EncryptedTextField(help_text=_("The confession text, encrypted in the DB."))
    
    # Optional image
    image = models.ImageField(upload_to='confessions/', blank=True, null=True)
    
    # Metadata
    mood = models.CharField(max_length=50, default='neutral', help_text=_("e.g., love, funny, angry"))
    
    # Safety fields
    ip_hash = models.CharField(max_length=64, help_text=_("SHA-256 hash of the sender's IP address"))
    is_read = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False, help_text=_("If recipient chooses to showcase this"))
    likes_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Confession for {self.recipient.username} ({self.created_at})"
