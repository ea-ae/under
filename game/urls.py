from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', views.game, name='main'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login')
]
