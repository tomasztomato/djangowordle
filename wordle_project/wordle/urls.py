from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('wordle/', views.wordle_game, name='wordle_game'),
    path('register/', views.register, name='register'),
]
