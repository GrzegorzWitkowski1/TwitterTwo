from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, RegisterUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .moderation import moderator


def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                tweet = form.save(commit=False)

                if (offence := moderator(tweet.body)) == 'Hate Speech':
                    messages.error(request, 'Your Tweet possibly contains hate speech and cannot be posted.')
                    return redirect('home')
                
                elif offence == 'Offensive Language':
                    tweet.is_offensive = True
                    tweet.user = request.user
                    tweet.save()
                    messages.success(request, ('Your Tweet possibly contains offensive speech and has been flagged.'))
                    messages.success(request, ('Your Tweet has been posted!'))

                elif offence == 'No Hate and Offensive':
                    tweet.user = request.user
                    tweet.save()
                    messages.success(request, ('Your Tweet has been posted!'))
                    return redirect('home')

        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'tweets': tweets, 'form': form})

    else:
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
    

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        
        else:
            messages.success(request, ('There was an error logging in!'))
            return redirect('login')

    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('home')


def register_user(request):
    form = RegisterUser()

    if request.method == 'POST':
        form = RegisterUser(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have succesfully registered!'))
            return redirect('home')

    return render(request, 'register.html', {'form': form})