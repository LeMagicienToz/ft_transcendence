from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import CustomUser
from .redis_client import r
import random
from django.core.mail import send_mail
from django.conf import settings
from os import path, makedirs
import requests, jwt



def utils_set_user_color(data, user): # la fonction ne save pas l'objet user
    suitColor = data.get('suitColor')
    visColor = data.get('visColor')
    ringsColor = data.get('ringsColor')
    bpColor = data.get('bpColor')

    colors_to_validate = {
        'suitColor': suitColor,
        'visColor': visColor,
        'ringsColor': ringsColor,
        'bpColor': bpColor
    }

    for color_name, color_value in colors_to_validate.items(): # items renvoie un tuple (clé, valeur)
        if color_value and (not color_value.startswith('#') or 
                            len(color_value) != 7 or 
                            not all(c in '0123456789ABCDEFabcdef' for c in color_value[1:])):
            return JsonResponse({'success': False, 'error': f'Couleur {color_name} invalide'}, status=400)

    try:
        custom_user = user.custom_user
        custom_user.suitColor = suitColor
        custom_user.visColor = visColor
        custom_user.ringsColor = ringsColor
        custom_user.bpColor = bpColor
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)
    return JsonResponse({'success': True, 'message': 'Couleurs mises à jour avec succès', 'user_id': user.id}, status=200)

def utils_set_username(data, user): # la fonction ne save pas l'objet user
    username = data.get('username')
    if username and (username.endswith('#42') or '@' in username):
        return JsonResponse({'success': False, 'error': 'Nom d\'utilisateur invalide'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'error': 'Nom d\'utilisateur déjà utilisé'}, status=400)
    if username:
        user.username = data.get('username')
    else:
        return JsonResponse({'success': False, 'error': 'username manquant'}, status=400)
    return JsonResponse({'success': True, 'message': 'Nom d\'utilisateur valide'}, status=200)

def utils_set_email(data, user): # la fonction ne save pas l'objet user
    email = data.get('email')
    if email and (email.endswith('@student.42.fr') or not '@' in email):
        return JsonResponse({'success': False, 'error': 'Email invalide'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'error': 'Email déjà utilisé'}, status=400)
    if email:
        user.email = data.get('email')
    else:
        return JsonResponse({'success': False, 'error': 'Email manquant'}, status=400)
    return JsonResponse({'success': True, 'message': 'Email valide'}, status=200)

# def email_is_confirmed(user):
#     if user.custom_user.email_confirmed == True:
#         return JsonResponse({'success': True, 'message': 'Email confirmé'}, status=200)
#     return JsonResponse({'success': False, 'error': 'Email non confirmé'}, status=400)

def utils_delete_account(user):
    user.custom_user.delete()
    user.delete()
    return JsonResponse({'success': True, 'message': 'Compte supprimé'}, status=200)

def utils_send_twoFA_code(user):
    twoFA_code = random.randint(100000, 999999)
    r.setex(f'user_{user.id}_twoFA_code', 300, twoFA_code) # 300 = 5 minutes
    send_mail(
        '2FA code',
        f'Your 2FA code is {twoFA_code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

# def utils_set_twoFA_verified(user, status, time_to_live=300):
#     r.setex(f"user:{user.id}:twoFA_verified", time_to_live, status)

# def utils_get_twoFA_verified(user):
#     return r.get(f"user:{user.id}:twoFA_verified")

def utils_reset_password(data, user): # la fonction ne save pas l'objet user
    username = data.get('username')
    new_password = data.get('new_password')

    if not new_password or not username:
        return JsonResponse({'success': False, 'error': 'username ou new_password manquant'}, status=400)

    if username and username.endswith('#42'):
        return JsonResponse({'success': False, 'error': 'Nom d\'utilisateur invalide'}, status=400)
    if username and '@' in username:
        user = User.objects.filter(email=username).first()
        username = user.username
    # user_exist = User.objects.get(username=user.username)
    # if not user_exist:
    #     return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)
    user.set_password(new_password)
    user.save()
    return JsonResponse({'success': True, 'message': 'Mot de passe réinitialisé avec succès', 'user_id': user.id}, status=200)

# ADDITION: A VERIFIER
def utils_upload_file(file, new_name):
    if not path.exists(settings.MEDIA_ROOT):
        makedirs(settings.MEDIA_ROOT)
    file_path = path.join(settings.MEDIA_ROOT, new_name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def utils_get_user(token, refresh_token, token42):
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                redis_token = r.get(f'user_{user.id}_token')
                if redis_token and redis_token.decode() != token:
                    return None
                return user
            else:
                return None
        except jwt.ExpiredSignatureError:
            pass
        except jwt.InvalidTokenError:
            return None
    
    if refresh_token:
        try:
            refresh_payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
            user_id = refresh_payload.get('user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                redis_refresh_token = r.get(f'user_{user.id}_refresh_token')
                if redis_refresh_token and redis_refresh_token.decode() != refresh_token:
                    return None
                return user
            else:
                return None
        except jwt.ExpiredSignatureError:
            return None

    if token42:
        try:
            headers = {'Authorization': f'Bearer {token42}'}
            response = requests.get(url="https://api.intra.42.fr/oauth/token/info", headers=headers)
            token_data = response.json()
            expires_in_seconds = token_data.get('expires_in_seconds')
            if expires_in_seconds is None or expires_in_seconds <= 0:
                return None
            user_info_response = requests.get(url=os.getenv('USER_URL'), headers=headers)
            user_data = user_info_response.json()
            intra_id = user_data.get('id')
            user = User.objects.filter(custom_user__intra_id=intra_id).first()
            if not user:
                return None
            redis_42_token = r.get(f'user_{user.custom_user.intra_id}_42_access_token')
            if redis_42_token and redis_42_token.decode() != token42:
                return None
            return user
        except requests.RequestException:
            return None
    return None

