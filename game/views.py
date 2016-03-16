from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import random


@require_http_methods(["GET"])
def index(request):
    return render(request, 'game/index.html', {})


@require_http_methods(["POST"])
def new_game(request):
    WORDS = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
    if request.POST.get('new_game') == '1':
        # Clean all session
        request.session.flush()
        # Get a new chosen_word
        ran = random.randint(0, (len(WORDS) - 1))
        chosen_word = WORDS[ran]
        # Save it into session
        request.session['chosen_word'] = chosen_word
        return JsonResponse({'new_game': '1'})
    return HttpResponse("Page not found", status=404)


@require_http_methods(["GET", "POST"])
def check_word(request):
    if not request.session.get('chosen_word'):
        return HttpResponse("Invalid request", status=405)

    # Letters that the user tried
    guessed_letter = request.session.get('guessed_letter', [])
    chosen_word = request.session['chosen_word'].upper()
    wrong_tries = request.session.get('wrong_tries', 0)
    letter = request.POST.get('letter')

    if letter and letter not in guessed_letter and wrong_tries < 5:
        guessed_letter.append(letter)
        if letter not in chosen_word:
            wrong_tries += 1
    request.session['wrong_tries'] = wrong_tries

    word_show = []
    hits = 0
    for i in xrange(0, len(chosen_word)):
        if chosen_word[i] in guessed_letter:
            word_show.append("%s " % chosen_word[i].upper())
            hits += 1
        else:
            word_show.append("_")
    request.session['guessed_letter'] = guessed_letter

    msg = ""
    status = 2  # Can stil play
    # User can only be wrong 5 times
    if wrong_tries >= 5:
        msg = 'Limit reached. You lose!'
        status = 0  # Lost the game

    # Check if user got all letter right
    if hits == len(chosen_word):
        msg = "Congratulations! You won."
        status = 1  # Won the game

    return JsonResponse({
        'word_show': ' '.join(word_show),
        'msg': msg,
        'remaining': str((5-wrong_tries)),
        'status': str(status),
        'guessed_letter': guessed_letter
    })
