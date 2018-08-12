from django.shortcuts import render, redirect, reverse


def game(request):
    # This is a slow solution for logging out the user of all other
    # active sessions, but it works.
    if request.user.is_authenticated and request.user.is_active:
        return render(request, 'game/game.html')
    else:
        return redirect(reverse('main:login') + '?next=' + request.path)
