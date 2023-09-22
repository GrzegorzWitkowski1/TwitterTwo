from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Tweet

def home(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.all().order_by('-created_at')
    
    return render(request, 'home.html', {'tweets': tweets})


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by('-created_at')

        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST['follow']

            if action == 'unfollow':
                current_user_profile.follows.remove(profile)

            elif action == 'follow':
                current_user_profile.follows.add(profile)

            current_user_profile.save()

        return render(request, 'profile.html', {'profile': profile,'tweets': tweets})
    
    else:
        messages.success(request, ('You must be logged in to view this page!'))
        return redirect('home')
    

def explore_profiles(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'explore_profiles.html', {'profiles': profiles})
    
    else:
        messages.success(request, ('You must be logged in to view this page!'))
        return redirect('home')