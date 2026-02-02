from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    slug = models.SlugField(unique=True, blank=True, null=True, help_text=_("Unique identifier for public profile"))
    is_shadow_banned = models.BooleanField(default=False, help_text=_("If true, user's confessions/actions are hidden from others"))
    preferences = models.JSONField(default=dict, blank=True, help_text=_("User preferences for theme, notifications, etc."))

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug and self.username:
            self.slug = self.username
        super().save(*args, **kwargs)
