from django.urls import path

from . import views


app_name = 'portofolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('experience/', views.home, name='experience'),
    path('profile/', views.profile_page, name='profile'),
]