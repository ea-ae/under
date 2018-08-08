from django.shortcuts import render, redirect
from .models import User, Profile
from .forms import CustomUserCreationForm
from . import blacklist
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'game/index.html')


def game(request):
    return render(request, 'game/index.html')


def register(request):
    error_msg = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['username'].lower() in blacklist.usernames:
                error_msg = 'That username is blacklisted!'
            elif User.objects.filter(username__iexact=form.cleaned_data['username']).exists():
                error_msg = 'A user with that username already exists.'
            else:
                form.save()
                if request.POST.get('remember_me'):
                    request.session.set_expiry(1209600)  # 2 weeks
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password2'])
                login(request, user)
                return redirect('game:main')
    else:
        form = CustomUserCreationForm()
    return render(request, 'game/register.html', {'form': form, 'user_error': error_msg})


def custom_login(request):
    return render(request, 'game/index.html')
