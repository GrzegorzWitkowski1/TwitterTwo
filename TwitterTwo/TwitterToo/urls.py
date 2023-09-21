from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore_profiles/', views.explore_profiles, name='explore_profiles'),
    path('profile/<int:pk>', views.profile, name='profile'),
]