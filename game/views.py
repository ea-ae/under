from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  # Does not fit our needs all the time
from .models import User, Profile
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from . import blacklist
from ratelimit.decorators import ratelimit
from django.urls import reverse


def index(request):
    return render(request, 'game/index.html')


def game(request):
    return render(request, 'game/index.html')


@ratelimit(key='header:x-real-ip', rate='10/10m', method='POST', block=True)
@ratelimit(key='ip', rate='10/10m', method='POST', block=True)
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


@ratelimit(key='header:x-real-ip', rate='15/5m', method='POST', block=True)
@ratelimit(key='ip', rate='15/5m', method='POST', block=True)
def custom_login(request):
    if request.method == 'POST':
        if request.POST.get('remember_me'):
            request.session.set_expiry(1209600)  # 2 weeks
    # response = auth_login(request, template_name=template_name, authentication_form=authentication_form)
    response = LoginView.as_view(template_name='game/login.html',
                                 authentication_form=CustomLoginForm)(request)
    return response


def logout(request):
    return render(request, 'game/logout.html')


def ratelimited(request):
    return render(request, 'ratelimit.html')
