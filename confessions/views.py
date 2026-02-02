from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Confession
from .forms import ConfessionForm
from hashlib import sha256

User = get_user_model()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

from moderation.service import ModerationService

def public_profile(request, slug):
    recipient = get_object_or_404(User, slug=slug)
    
    if request.method == 'POST':
        form = ConfessionForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content_encrypted') # It's just text here before saving
            
            # Moderation Check
            if ModerationService.contains_profanity(content):
                messages.error(request, "Let's keep it safe. Please remove inappropriate language.")
                return render(request, 'confessions/public_profile.html', {'recipient': recipient, 'form': form})

            confession = form.save(commit=False)
            confession.recipient = recipient
            
            # IP Hashing
            ip = get_client_ip(request)
            ip_hash = sha256(ip.encode()).hexdigest()
            confession.ip_hash = ip_hash
            # confession.ip_hash = 'debug_hash'
            
            confession.save()
            messages.success(request, "Sent! 🚀")
            return redirect('public_profile', slug=slug)
    else:
        form = ConfessionForm()
    
    return render(request, 'confessions/public_profile.html', {'recipient': recipient, 'form': form})

@login_required
def dashboard(request):
    confessions = Confession.objects.filter(recipient=request.user).order_by('-is_pinned', '-created_at')
    return render(request, 'confessions/dashboard.html', {'confessions': confessions})

@login_required
def dashboard_grid(request):
    confessions = Confession.objects.filter(recipient=request.user).order_by('-is_pinned', '-created_at')
    return render(request, 'confessions/partials/confession_grid.html', {'confessions': confessions})

@login_required
def pin_confession(request, pk):
    confession = get_object_or_404(Confession, pk=pk, recipient=request.user)
    confession.is_pinned = not confession.is_pinned
    confession.save()
    
    if request.htmx:
        return render(request, 'confessions/partials/confession_card.html', {'confession': confession})
    return redirect('dashboard')

@login_required
def delete_confession(request, pk):
    confession = get_object_or_404(Confession, pk=pk, recipient=request.user)
    confession.delete()
    
    if request.htmx:
        return HttpResponse("")
    return redirect('dashboard')
