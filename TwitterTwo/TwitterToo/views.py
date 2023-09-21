from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile

def home(request):
    return render(request, 'home.html', {})

def explore_profiles(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'explore_profiles.html', {'profiles': profiles})
    else:
        messages.success(request, ('You must be logged in to view this page!'))
        return redirect('home')