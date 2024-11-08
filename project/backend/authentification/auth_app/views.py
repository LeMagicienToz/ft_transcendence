import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser
from django.contrib.auth.models import User
from .decorators import jwt_required
import jwt, time, requests
from django.conf import settings
from django.shortcuts import redirect
from .decorators import jwt_42_required
from .decorators import request_from_42_or_regular_user, twoFA_status_check
from .utils_views import utils_set_user_color, utils_set_username, utils_set_email, utils_delete_account, utils_send_twoFA_code, utils_reset_password
import os
from django.core.mail import send_mail
from .redis_client import r
# mettre toute l'app asynchrone ???????????


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
        email = user_data.get('email')
        #image_url = user_data['image']['link'] # you can set different size of image by adding [versions][large/medium/small], see 42 api doc 
        image_url = user_data['image']['versions']['small'] # ['micro', 'small', 'medium', 'large']

        user = User.objects.filter(custom_user__intra_id=intra_id).first()
        #return JsonResponse({'success': True, 'message': 'testtttttttttttttttt', 'user_id': user.id, 'username': username, 'custom_user_intra_id': user.custom_user.intra_id}, status=200)
        if user is None:
            first_connection = True
        else:
            first_connection = False
        # if first_connection:
        #     user = User(username=username)
        #     user.email = email
        #     user.set_unusable_password()
        #     user.save()

        # custom_user, created = CustomUser.objects.get_or_create(user=user)
        # custom_user.profile_picture_url = image_url
        # custom_user.intra_id = intra_id
        # custom_user.twoFA_enabled = False
        # if first_connection:
        #     custom_user.suitColor = ''
        #     custom_user.visColor = ''
        #     custom_user.ringsColor = ''
        #     custom_user.bpColor = ''
        #     custom_user.twoFA_enabled = False
        #     custom_user.save()


        if first_connection:
            user = User(username=username, email=email)
            user.set_unusable_password()
            custom_user = CustomUser(user=user)
            custom_user.intra_id = intra_id
            custom_user.profile_picture_url = image_url
            custom_user.twoFA_enabled = False
        else:
            custom_user = CustomUser.objects.get(user=user)
            custom_user.profile_picture_url = image_url
            custom_user.intra_id = intra_id
        
        user.save()
        custom_user.save()

        #login(request, user)
        if user.custom_user.twoFA_enabled:
            utils_send_twoFA_code(user)
        #return JsonResponse({'success': True, 'message': 'Authentification réussie', 'user_id': user.id, 'username': user.username, 'profile_picture_url': image_url}, status=200)
        if first_connection:
            response = redirect(f'https://{os.getenv("HOST_SERVERNAME")}:8443/Avatar/')
        else:
            response = redirect(f'https://{os.getenv("HOST_SERVERNAME")}:8443/Home/')
        response.set_cookie('42_access_token', access_token, httponly=True, secure=True, samesite='Strict')
        r.setex(f'user_{user.custom_user.intra_id}_42_access_token', 60 * 60 * 24 * 7, access_token)
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
    if username and '@' in username:
        user = User.objects.filter(email=username).first()
        if user:
            user = authenticate(request, username=user.username, password=password)
    else:
        user = authenticate(request, username=username, password=password)
    if user is not None:
        #login(request, user)
        token = jwt.encode({'user_id': user.id, 'iat': int(time.time()), 'exp': int(time.time()) + 60 * 5}, settings.SECRET_KEY, algorithm='HS256')
        refresh_token = jwt.encode({'user_id': user.id, 'iat': int(time.time()), 'exp': int(time.time()) + 60 * 60 * 24 * 7}, settings.REFRESH_TOKEN_SECRET, algorithm='HS256')
        r.setex(f'user_{user.id}_token', 60 * 5, token)
        r.setex(f'user_{user.id}_refresh_token', 60 * 60 * 24 * 7, refresh_token)

        response = JsonResponse({'success': True, 'user_id': user.id, 'twoFA_enabled': user.custom_user.twoFA_enabled, 'profile_picture_url': user.custom_user.profile_picture_url, 'message': 'Utilisateur connecté avec succès'}, status=200)
        response.set_cookie(key='token', value=token, httponly=True, secure=True, samesite='Strict', max_age=60 * 5) # secure for https only, samesite for csrf protection, max_age 5 min
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=True, samesite='Strict', max_age=60 * 60 * 24 * 7)

        if user.custom_user.twoFA_enabled:
            utils_send_twoFA_code(user)
        return response
    else:
        return JsonResponse({'success': False, 'error': 'Identifiants invalides'}, status=400)
        

@request_from_42_or_regular_user
@require_POST
@twoFA_status_check
def logout_user(request):
    user = request.user
    r.delete(f'user_{user.id}_token')
    r.delete(f'user_{user.id}_refresh_token')
    r.delete(f'user_{user.custom_user.intra_id}_42_access_token')

    r.delete(f'user_{user.id}_twoFA_code')
    r.delete(f'user_{user.id}_twoFA_verified')
    response = JsonResponse({'success': True, 'message': 'Utilisateur déconnecté'}, status=200)
    response.delete_cookie('token')
    response.delete_cookie('refresh_token')
    response.delete_cookie('42_access_token')
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
    if email and (email.endswith('@student.42.fr' or not '@' in email)):
        return JsonResponse({'success': False, 'error': 'Email invalide'}, status=400)
    if username and (username.endswith('#42') or '@' in username):
        return JsonResponse({'success': False, 'error': 'Nom d\'utilisateur invalide'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'error': 'Email déjà utilisé'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'error': 'Nom d\'utilisateur déjà utilisé'}, status=400)       
    
    user = User.objects.create_user(username=username, password=password, email=email)
    custom_user = CustomUser(user=user)
    custom_user.intra_id = None
    custom_user.profile_picture_url = None
    custom_user.suitColor = ''
    custom_user.visColor = ''
    custom_user.ringsColor = ''
    custom_user.bpColor = ''
    custom_user.twoFA_enabled = False
    custom_user.flatness = 2.8
    custom_user.horizontalPosition = 0.73
    custom_user.verticalPosition = 0.08
    custom_user.visTexture = None
    custom_user.save()

    #login(request, user)
    token = jwt.encode({'user_id': user.id, 'iat': int(time.time()), 'exp': int(time.time()) + 60 * 5}, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode({'user_id': user.id, 'iat': int(time.time()), 'exp': int(time.time()) + 60 * 60 * 24 * 7}, settings.REFRESH_TOKEN_SECRET, algorithm='HS256')
    r.setex(f'user_{user.id}_token', 60 * 5, token)
    r.setex(f'user_{user.id}_refresh_token', 60 * 60 * 24 * 7, refresh_token)

    response = JsonResponse({'success': True, 'message': f"Utilisateur {user.username} créé avec succès + login!", 'user_id': user.id}, status=201)
    response.set_cookie(key='token', value=token, httponly=True, secure=True, samesite='Strict', max_age=60 * 5)  # sécurisé
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=True, samesite='Strict', max_age=60 * 60 * 24 * 7)
 
    return response


@require_POST
@request_from_42_or_regular_user
@twoFA_status_check
def delete_account(request):
    user = request.user
    user.custom_user.delete()
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
@require_GET
@twoFA_status_check
def get_user(request):
    user = request.user
    username = user.username
    profile_picture_url = user.custom_user.profile_picture_url
    flatness = user.custom_user.flatness
    horizontalPosition = user.custom_user.horizontalPosition
    verticalPosition = user.custom_user.verticalPosition
    visTexture = user.custom_user.visTexture
    flatness = user.custom_user.flatness
    horizontalPosition = user.custom_user.horizontalPosition
    verticalPosition = user.custom_user.verticalPosition
    suitColor = user.custom_user.suitColor
    visColor = user.custom_user.visColor
    ringsColor = user.custom_user.ringsColor
    bpColor = user.custom_user.bpColor
    return JsonResponse({'success': True, 'user_id': user.id, 'username': username, 'profile_picture_url': profile_picture_url, 'flatness': flatness, 'horizontalPosition': horizontalPosition, 'verticalPosition': verticalPosition, 'visTexture': visTexture, 'suitColor': suitColor, 'visColor': visColor, 'ringsColor': ringsColor, 'bpColor': bpColor}, status=200)

@request_from_42_or_regular_user
@require_POST
@twoFA_status_check
def set_user_color(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Corps de la requête invalide ou manquant'}, status=400)
    user = request.user
    response = utils_set_user_color(data, user)
    user.custom_user.flatness = data.get('flatness', 2.8)
    user.custom_user.horizontalPosition = data.get('horizontalPosition', 0.73)
    user.custom_user.verticalPosition = data.get('verticalPosition', 0.08)
    user.custom_user.visTexture = data.get('visTexture', None)
    user.custom_user.save()
    user.save()
    return response


@request_from_42_or_regular_user
@require_POST
@twoFA_status_check
def set_profile(request): # username, email, twoFA_enabled, new_password
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'profile: Corps de la requête invalide ou manquant'}, status=400)
    user = request.user
    #username
    response = utils_set_username(data, user)
    if response.get('success') == False:
        return response
    #email
    response = utils_set_email(data, user)
    if response.get('success') == False:
        return response
    #password
    response = utils_reset_password(data, user)
    if response.get('success') == False:
        return response
    # set twoFA
    twoFA_enabled = data.get('twoFA_enabled')
    if twoFA_enabled == True:
        user.custom_user.twoFA_enabled = True
    else:
        user.custom_user.twoFA_enabled = False

    user.custom_user.save()
    user.save()
    return JsonResponse({'success': True, 'message': 'Profil mis à jour avec succès', 'user_id': user.id}, status=200)

#     @require_GET
# def confirm_email(request):
#     token = request.GET.get('token')

#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#         user_id = payload['user_id']
#         user = User.objects.get(id=user_id)
        
#         user.custom_user.email_confirmed = True
#         user.custom_user.save()
        
#         # return JsonResponse({'success': True, 'message': 'E-mail confirmé avec succès.'}, status=200)
#         return redirect('https://${HOST_SERVERNAME}:8443/home/')
#     except (jwt.ExpiredSignatureError):
#         utils_delete_account(user)
#         return edirect('https://${HOST_SERVERNAME}:8443/login/')
#         # return JsonResponse({'success': False, 'error': 'Lien de confirmation expiré, inscrivez-vous à nouveau'}, status=400)
#     except jwt.InvalidTokenError:
#         return redirect('https://${HOST_SERVERNAME}:8443/login/')
#         # return JsonResponse({'success': False, 'error': 'Lien de confirmation invalide'}, status=400)
#     except User.DoesNotExist:
#         return redirect('https://${HOST_SERVERNAME}:8443/login/')
        # return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)

@require_POST
@jwt_required
def twoFA_validation(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Corps de la requête invalide ou manquant'}, status=400)

    user = request.user
    twoFA_code = data.get('twoFA_code')
    
    if not twoFA_code:
        return JsonResponse({'success': False, 'error': 'Code 2FA manquant ou invalide'}, status=400)

    redis_code = r.get(f'user_{user.id}_twoFA_code')
    if redis_code is None:
        return JsonResponse({'success': False, 'error': 'Code 2FA non trouvé'}, status=404)
    
    if redis_code.decode('utf-8') == twoFA_code: # ne pas oublier de decoder se qui vient de redis
        r.set(f'user_{user.id}_twoFA_verified', 'True')
        return JsonResponse({'success': True, 'message': 'Code 2FA validé avec succès'}, status=200)
    return JsonResponse({'success': False, 'error': 'Code 2FA invalide'}, status=400)

@require_POST
@request_from_42_or_regular_user
@twoFA_status_check
def search_user(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Corps de la requête invalide ou manquant'}, status=400)
    username = data.get('username')
    if not username:
        return JsonResponse({'success': False, 'error': 'username manquant'}, status=400)
    user = User.objects.filter(username=username).first()
    if not user:
        return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)
    return JsonResponse({'success': True, 'message': 'Utilisateur trouvé', 'user_id': user.id, 'username': user.username, 'profile_picture_url': user.custom_user.profile_picture_url}, status=200)
    

@require_POST
@request_from_42_or_regular_user
@twoFA_status_check
def add_friend(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Corps de la requête invalide ou manquant'}, status=400)
    username = data.get('username')
    if not username:
        return JsonResponse({'success': False, 'error': 'username manquant'}, status=400)
    friend = User.objects.filter(username=username).first()
    if not friend:
        return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)
    user = request.user
    if user.custom_user.friends_list.filter(id=friend.custom_user.id).exists():
        return JsonResponse({'success': False, 'error': 'Ami déjà ajouté'}, status=400)
    user.custom_user.friends_list.add(friend.custom_user)
    return JsonResponse({'success': True, 'message': 'Ami ajouté avec succès', 'user_id': user.id}, status=200)

@require_POST
@request_from_42_or_regular_user
@twoFA_status_check
def remove_friend(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Corps de la requête invalide ou manquant'}, status=400)
    username = data.get('username')
    if not username:
        return JsonResponse({'success': False, 'error': 'username manquant'}, status=400)
    friend = User.objects.filter(username=username).first()
    if not friend:
        return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)
    user = request.user
    user.custom_user.friends_list.remove(friend.custom_user)
    return JsonResponse({'success': True, 'message': 'Ami supprimé avec succès', 'user_id': user.id}, status=200)

@require_POST
@request_from_42_or_regular_user
@twoFA_status_check
def get_friends_list(request):
    user = request.user
    friends_list = user.custom_user.friends_list.all()
    friends = [{'username': friend.user.username, 'profile_picture_url': friend.profile_picture_url} for friend in friends_list]
    return JsonResponse({'success': True, 'friends': friends}, status=200)






    
    




    
    


