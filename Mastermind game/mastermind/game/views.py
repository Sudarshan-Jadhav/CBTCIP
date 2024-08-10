from django.shortcuts import render, redirect, get_object_or_404
from .models import Game, Attempt
from django.utils import timezone

def index(request):
    game = Game.objects.order_by('-created_at').first()
    if not game:
        game = Game()
        game.generate_code()

    if request.method == 'POST':
        guess = request.POST.get('guess').upper()
        result = game.check_guess(guess)
        Attempt.objects.create(
            game=game,
            guess=guess,
            correct=result['correct'],
            wrong_position=result['wrong_position'],
            attempted_at=timezone.now()
        )
        return redirect('index')

    attempts = game.attempts.all()

    return render(request, 'game/index.html', {
        'game': game,
        'attempts': attempts
    })

def reset_game(request):
    Game.objects.all().delete()
    return redirect('index')
