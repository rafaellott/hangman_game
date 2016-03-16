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

    word_show = ""
    for i in xrange(0, len(chosen_word)):
        word_show += "_ "
    return JsonResponse({'word_show': word_show})


@require_http_methods(["GET", "POST"])
def check_word(request):
    if request.method == 'POST':
        ch = request.GET.get('ch')
        s = request.GET.get('s')
        if not ch or not s:
            return HttpResponse("Invalid request", status=405)
        positions = [i+1 for i, ltr in enumerate(s) if ltr == ch]
        return JsonResponse({'pos': positions})
    elif request.method == 'GET':
        return JsonResponse({'foo': 'bar'})
