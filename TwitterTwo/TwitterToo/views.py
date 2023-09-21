from django.shortcuts import render
from .models import Profile

def home(request):
    return render(request, 'home.html', {})

def explore_profiles(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'explore_profiles.html', {'profiles': profiles})