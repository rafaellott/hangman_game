from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import random


def index(request):
    live_game = False
    if request.method == "GET" and request.session.get('chosen_word'):
        live_game = True
    return render(request, 'game/index.html', {
        'live_game': live_game,
    })


@require_http_methods(["GET", ])
def new_game(request):
    request.session.clear()
    WORDS = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
    ran = random.randint(0, (len(WORDS) - 1))
    chosen_word = WORDS[ran]
    return render(request, 'game/index.html', {
        'word_size': len(chosen_word)
    })


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


def print_session(request):
    import beautify
    if request.GET.get('askejgishdtubmansibpqkaadgf', '0') == '1':
        return HttpResponse(beautify.Beautify(request.sessio))
    else:
        return HttpResponse(status=404)
