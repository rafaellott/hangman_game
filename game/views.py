from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


def index(request):
    return render(request, 'game/index.html', {})


def check_word(request):
    if request.method == 'POST':
        return JsonResponse({'foo': 'bar'})
    else:
        return HttpResponse(status=405)
