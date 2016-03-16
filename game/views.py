from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import random


@require_http_methods(["GET"])
def index(request):
    return render(request, 'game/index.html', {})


@require_http_methods(["GET", "POST"])
def get_game(request):
    WORDS = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
    if request.method == 'GET':
        if not request.session.get('chosen_word'):
            ran = random.randint(0, (len(WORDS) - 1))
            chosen_word = WORDS[ran]
            request.session['chosen_word'] = chosen_word
        else:
            chosen_word = request.session['chosen_word']
    elif request.method == 'POST':
        request.session.flush()
        ran = random.randint(0, (len(WORDS) - 1))
        chosen_word = WORDS[ran]
        request.session['chosen_word'] = chosen_word

    guessed_letter = request.session.get('guessed_letter', [])
    word_show = []
    hits = 0
    for i in xrange(0, len(chosen_word)):
        if chosen_word[i] in guessed_letter:
            word_show.append("%s " % chosen_word[i].upper())
            hits += 1
        else:
            word_show.append("_")
    return JsonResponse({'word_show': ' '.join(word_show), })


@require_http_methods(["POST"])
def check_word(request):
    if not request.session.get('chosen_word'):
        return HttpResponse("Invalid request", status=405)

    # Letters that the user tried
    guessed_letter = request.session.get('guessed_letter', [])
    chosen_word = request.session['chosen_word'].upper()
    letter = request.POST.get('letter')

    if letter not in guessed_letter:
        guessed_letter.append(letter)

    word_show = []
    hits = 0
    tries = 0
    for i in xrange(0, len(chosen_word)):
        if chosen_word[i] in guessed_letter:
            word_show.append("%s " % chosen_word[i].upper())
            hits += 1
        else:
            word_show.append("_")
    request.session['guessed_letter'] = guessed_letter

    for a in guessed_letter:
        if a not in chosen_word:
            tries += 1

    msg = ""
    status = 2
    # User can only be wrong 5 times
    if tries >= 5:
        msg = 'Limit reached. You lose!'
        status = 0

    # Check if user got all letter right
    if hits == len(chosen_word):
        msg = "Congratulations! You won."
        status = 1
    print tries
    return JsonResponse({
        'word_show': ' '.join(word_show),
        'msg': msg,
        'remaining': str((5-tries)),
        'status': str(status)
    })
