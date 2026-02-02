from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Report(models.Model):
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('harassment', 'Harassment or Bullying'),
        ('hate', 'Hate Speech'),
        ('nsfw', 'Inappropriate Content'),
        ('other', 'Other'),
    ]

    confession = models.ForeignKey('confessions.Confession', on_delete=models.CASCADE, related_name='reports')
    reporter_ip_hash = models.CharField(max_length=64, blank=True, null=True)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolution_note = models.TextField(blank=True)

    def __str__(self):
        return f"Report {self.id} - {self.reason}"

class BlockedIP(models.Model):
    ip_hash = models.CharField(max_length=64, unique=True)
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.ip_hash
