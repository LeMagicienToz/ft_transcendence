import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser
from django.contrib.auth.models import User
from .decorators import jwt_required


def login_42(request):
    login_url = f"{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    return redirect(login_url)

def callback_42(request):
    code = request.GET.get('code')
    
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    
    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    if access_token:
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(USER_URL, headers=headers)
        user_data = user_response.json()

        username = user_data.get('login') + '#42'
        intra_id = user_data.get('id')
        image_url = user_data.get('image_url')

        user = User.objects.filter(id=intra_id).first()

        if not user:
            user = User(username=username)
            user.set_unusable_password()
            user.save()

        custom_user, created = CustomUser.objects.get_or_create(user=user)
        custom_user.profile_picture_url = image_url
        custom_user.is_online = True
        custom_user.intra_id = intra_id
        custom_user.save()

        login(request, user)

        #envoyer a game api les infos de l'utilisateur ---------------------------------------------------------------

        return JsonResponse({'success': True, 'message': 'Authentification réussie', 'user_id': user.id, 'username': user.username, 'profile_picture_url': image_url}, status=200)
    return JsonResponse({'success': False, 'error': 'Échec de l\'authentification'}, status=400)

@require_POST
def login_user(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'success': False, 'error': 'Corps de la requête invalide ou manquant'}, status=400)
    user = authenticate(request, username=username, password=password) # verifier si ca protege d'un user qui se connecte a un compte 42 mdp vide
    if user is not None:
        login(request, user)
        user.customuser.is_online = True
        user.customuser.save()
        token = jwt.encode({'user_id': user.id, 'iat': int(time.time()), 'exp': int(time.time()) + 60 * 5}, settings.SECRET_KEY, algorithm='HS256')
        refresh_token = jwt.encode({'user_id': user.id, 'iat': int(time.time()), 'exp': int(time.time()) + 60 * 60 * 24 * 7}, settings.REFRESH_SECRET_KEY, algorithm='HS256')
        return JsonResponse({'success': true,'token': token, 'refresh_token': refresh_token, 'user_id': user.id}, status=200)
    else:
        return JsonResponse({'success': False, 'error': 'Identifiants invalides'}, status=400)
        

@login_required
@jwt_required
@require_POST
def logout_user(request):
    user = request.user
    user.customuser.is_online = False
    user.customuser.save()
    logout(request)
    return JsonResponse({'success': True, 'message': 'Déconnexion réussie'}, status=200)

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
    user = User.objects.create_user(username=username, password=password)
    custom_user = CustomUser(user=user)
    custom_user.intra_id = None
    custom_user.profile_picture_url = None
    custom_user.save()
    return JsonResponse({'success': True, 'message': f"Utilisateur {user.username} créé avec succès!", 'user_id': user.id}, status=201)


@require_POST
@login_required
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
@login_required
@jwt_required
def delete_account(request):
    try:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)

    user.delete()
    return JsonResponse({'success': True,'message': 'Compte supprimé avec succès'}, status=200)

