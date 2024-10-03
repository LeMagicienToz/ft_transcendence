from django.shortcuts import render
from django.views.decorators.http import require_POST

@require_POST
def receive_user(request):
        return JsonResponse({'received': 'ok'})