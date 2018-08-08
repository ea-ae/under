from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', views.game, name='main'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(template_name='game/logout.html'), name='logout')
]
