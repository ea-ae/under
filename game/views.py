from django.shortcuts import render


def game(request):
    if request.user.is_authenticated and request.user.is_active:
        return render(request, 'game/game.html')
    else:
        return redirect(reverse('game:login') + '?next=' + request.path)
