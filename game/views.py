from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from game.service import HangmanGame
import random

WORDS = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']


@require_http_methods(["GET"])
def index(request):
    game = HangmanGame() if not request.session.get('game') \
        else HangmanGame(request.session['game'])
    request.session['game'] = game.storage
    return render(request, 'game/index.html', {
        'match': 'resume'
    })


@require_http_methods(["POST"])
def new_game(request):
    if request.POST.get('new_game') == '1':
        # Clean all session
        request.session.flush()
        game = HangmanGame()
        request.session['game'] = game.storage
        return JsonResponse({'new_game': '1'})
    return HttpResponse("Page not found", status=404)


@require_http_methods(["POST", "GET"])
def check_word(request):
    if not request.session.get('game', {}).get('chosen_word'):
        return JsonResponse(
            {'msg': 'Invalid game. Start a new one.'}, status=400
        )

    if request.method == "GET":
        game = HangmanGame(request.session['game'])
        reply = game.state()
    elif not request.POST.get('letter'):
        return JsonResponse(
            {'msg': 'Invalid game. Start a new one.'}, status=400
        )
    else:
        game = HangmanGame(request.session['game'])
        reply = game.check_letter(request.POST.get('letter').lower())
        request.session['game'] = game.storage
    return JsonResponse({
        'word_show': reply['draw'],
        'msg': reply['msg'],
        'remaining': (5 - reply['wrong_tries']),
        'won': game.win(),
        'guessed_letter': reply['letter_used'],
    })


def clear_session(request):
    request.session.flush()
    return redirect('index')
