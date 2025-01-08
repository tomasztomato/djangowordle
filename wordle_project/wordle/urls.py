from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('wordle/', views.game_view, name='wordle'),
    path('register/', views.register_view, name='register'),
]
