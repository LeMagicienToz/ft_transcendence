import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser
from django.contrib.auth.models import User
from .decorators import jwt_required
import jwt, time, requests
from django.conf import settings
from django.shortcuts import redirect
from .decorators import jwt_42_required
from .decorators import request_from_42_or_regular_user
import os

def login_42(request):
    login_url = f"{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    login_url = f'{os.getenv("AUTH_URL")}?client_id={os.getenv("API_42_CLIENT_ID")}&redirect_uri={os.getenv("CALLBACK_URL_YOU_SET_ON_42")}&response_type=code'
    return redirect(login_url)

def callback_42(request):
    code = request.GET.get('code')
    
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': os.getenv('API_42_CLIENT_ID'),
        'client_secret': os.getenv('API_42_CLIENT_SECRET'),
        'code': code,
        'redirect_uri': os.getenv('CALLBACK_URL_YOU_SET_ON_42')
    }
    
    token_response = requests.post(url=os.getenv('TOKEN_URL'), data=token_data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    if access_token:
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(url=os.getenv('USER_URL'), headers=headers)
        user_data = user_response.json()

        username = user_data.get('login') + '#42'
        intra_id = user_data.get('id')
        #image_url = user_data['image']['link'] # you can set different size of image by adding [versions][large/medium/small], see 42 api doc 
        image_url = user_data['image']['versions']['small'] # ['micro', 'small', 'medium', 'large']

        user = User.objects.filter(username=username).first()
        first_connection = False
        if not user:
            first_connection = True
            user = User(username=username)
            user.set_unusable_password()
            user.save()

        custom_user, created = CustomUser.objects.get_or_create(user=user)
        custom_user.profile_picture_url = image_url
        custom_user.is_online = True
        custom_user.intra_id = intra_id
        custom_user.save()

        login(request, user)
        #return JsonResponse({'success': True, 'message': 'Authentification réussie', 'user_id': user.id, 'username': user.username, 'profile_picture_url': image_url}, status=200)
        if first_connection:
            response = redirect('https://localhost:8443/Avatar/')
        else:
            response = redirect('https://localhost:8443/Homepage/')
        response.set_cookie('42_access_token', access_token, httponly=True, secure=True, samesite='Strict')
        return response
    return JsonResponse({'success': False, 'error': 'Échec de l\'authentification'}, status=400)


@require_POST
def login_user(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'success': False, 'error': 'Corps de la requête invalide ou manquant'}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # user.customuser.is_online = True
        # user.customuser.save()
        token = jwt.encode({'user_id': user.id, 'iat': int(time.time()), 'exp': int(time.time()) + 60 * 5}, settings.SECRET_KEY, algorithm='HS256')
        refresh_token = jwt.encode({'user_id': user.id, 'iat': int(time.time()), 'exp': int(time.time()) + 60 * 60 * 24 * 7}, settings.REFRESH_TOKEN_SECRET, algorithm='HS256')
        response = JsonResponse({'success': True, 'user_id': user.id, 'message': 'connecté'}, status=200)
        response.set_cookie(key='token', value=token, httponly=True, secure=True, samesite='Strict', max_age=60 * 5) # secure for https only, samesite for csrf protection, max_age 5 min
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=True, samesite='Strict', max_age=60 * 60 * 24 * 7)
        return response
    else:
        return JsonResponse({'success': False, 'error': 'Identifiants invalides'}, status=400)
        

@jwt_required
@require_POST
def logout_user(request):
    response = JsonResponse({'success': True, 'message': 'Utilisateur déconnecté'}, status=200)
    response.delete_cookie('token')
    response.delete_cookie('refresh_token')
    return response

@require_POST
def register(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Corps de la requête invalide ou manquant'}, status=400)

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return JsonResponse({'success': False, 'error': 'username, password ou email manquant'}, status=400)
    if email and email.endswith('@student.42.fr'):
        return JsonResponse({'success': False, 'error': 'Email invalide'}, status=400) 
    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'error': 'Nom d\'utilisateur déjà utilisé'}, status=400)       
    user = User.objects.create_user(username=username, password=password, email=email)
    custom_user = CustomUser(user=user)
    custom_user.intra_id = None
    custom_user.profile_picture_url = None
    custom_user.save()
    return JsonResponse({'success': True, 'message': f"Utilisateur {user.username} créé avec succès!", 'user_id': user.id}, status=201)


@require_POST
@jwt_required
def reset_password(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Corps de la requête invalide ou manquant'}, status=400)

    username = data.get('username')
    new_password = data.get('new_password')

    if not new_password:
        return JsonResponse({'success': False, 'error': 'Nouveau mot de passe manquant'}, status=400)

    if username and username.endswith('#42'):
        return JsonResponse({'success': False, 'error': 'Nom d\'utilisateur invalide'}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)

    user.set_password(new_password)
    user.save()
    return JsonResponse({'success': True, 'message': 'Mot de passe réinitialisé avec succès', 'user_id': user.id}, status=200)


@require_POST
@jwt_required
def delete_account(request):
    try:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)

    user.delete()
    return JsonResponse({'success': True,'message': 'Compte supprimé avec succès'}, status=200)


# def send_user_info(user):
#     api_key = os.getenv('GAME_API_KEY')
    
#     headers = {
#         'Authorization': f'Api-Key {api_key}',
#         'Content-Type': 'application/json'
#     }
#     data = {'user_id': user.id}
#     response = requests.post('http://game:8001/api/game/users/', headers=headers, data=json.dumps(data))
    
#     return response.json()

@request_from_42_or_regular_user
def get_user(request):
    user = request.user
    username = user.username
    profile_picture_url = user.customuser.profile_picture_url
    return JsonResponse({'success': True, 'username': username, 'profile_picture_url': profile_picture_url}, status=200)



    
    


