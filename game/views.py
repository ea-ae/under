from django.shortcuts import render, redirect


def index(request):
    return render(request, 'game/index.html')


def game(request):
    return render(request, 'game/index.html')


def register(request):
    return render(request, 'game/index.html')


def login(request):
    return render(request, 'game/index.html')
