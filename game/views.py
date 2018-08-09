from django.shortcuts import render, redirect, reverse


def game(request):
    if request.user.is_authenticated and request.user.is_active:
        return render(request, 'game/game.html')
    else:
        return redirect(reverse('main:login') + '?next=' + request.path)
