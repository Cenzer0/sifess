from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from confessions.models import Confession
from moderation.service import ModerationService

User = get_user_model()

class SIFESSTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123', slug='testuser')
        self.url = reverse('public_profile', args=['testuser'])

    def test_send_confession(self):
        response = self.client.post(self.url, {
            'content_encrypted': 'You are awesome!',
            'mood': 'happy'
        })
        self.assertEqual(response.status_code, 302) # Redirects on success
        self.assertEqual(Confession.objects.count(), 1)
        confession = Confession.objects.first()
        self.assertEqual(confession.content_encrypted, 'You are awesome!')

    def test_profanity_filter(self):
        # Assuming 'badword' is caught by better_profanity default list? 
        # actually default list contains standard english bad words. 'fuck' is one.
        response = self.client.post(self.url, {
            'content_encrypted': 'You are a fuck',
            'mood': 'angry'
        })
        self.assertEqual(response.status_code, 200) # Re-renders form with error
        self.assertEqual(Confession.objects.count(), 0)
        self.assertContains(response, "inappropriate language")

    def test_dashboard_access(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_pin_confession(self):
        confession = Confession.objects.create(
            recipient=self.user, 
            content_encrypted='Pin me', 
            ip_hash='123'
        )
        self.client.login(username='testuser', password='password123')
        
        url = reverse('pin_confession', args=[confession.id])
        self.client.post(url)
        
        confession.refresh_from_db()
        self.assertTrue(confession.is_pinned)

    def test_delete_confession(self):
        confession = Confession.objects.create(
            recipient=self.user, 
            content_encrypted='Delete me', 
            ip_hash='123'
        )
        self.client.login(username='testuser', password='password123')
        
        url = reverse('delete_confession', args=[confession.id])
        self.client.post(url)
        
        self.assertEqual(Confession.objects.count(), 0)
