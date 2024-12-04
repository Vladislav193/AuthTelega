import json
import secrets
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

User = get_user_model()

def login_page(request):
    unique_token = secrets.token_urlsafe()
    cache.set(unique_token, unique_token, timeout=300)
    return render(request, 'login.html', {'unique_token': unique_token})


@csrf_exempt
def telega_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        telega_id = data.get("telegram_id")
        auth_token = data.get('auth_token')
        session_token = cache.get(auth_token)
        if auth_token != session_token:
            return JsonResponse({'error': 'Invalid token'}, status=400)
        cache.delete(auth_token)
        user, created = User.objects.get_or_create(telega_id=telega_id)
        if created:
            user.username = data.get('telegram_username')
            user.save()

        login(request, user)
        return redirect('home')
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def home(request):
    username = request.user.username
    return render(request, 'home.html', {'username': username})