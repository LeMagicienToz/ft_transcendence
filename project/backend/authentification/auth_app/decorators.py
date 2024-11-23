import jwt
import requests
from django.conf import settings
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth.models import User
from .redis_client import r
import time
import os
import time
from django.core.exceptions import ObjectDoesNotExist

def jwt_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        access_token = request.COOKIES.get('token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                request.user = User.objects.get(id=payload['user_id'])
                redis_token = r.get(f'user_{request.user.id}_token')
                if redis_token and redis_token.decode() != access_token:
                    return JsonResponse({'success': False, 'error': 'Access token révoqué'}, status=401)
                return view_func(request, *args, **kwargs)

            except ObjectDoesNotExist:
                return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)
            except jwt.ExpiredSignatureError:
                pass
            except jwt.InvalidTokenError:
                return JsonResponse({'success': False, 'error': 'Access token invalide'}, status=400)

        if refresh_token:
            try:
                refresh_payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
                request.user = User.objects.get(id=refresh_payload['user_id'])
                redis_refresh_token = r.get(f'user_{request.user.id}_refresh_token')
                if redis_refresh_token and redis_refresh_token.decode() != refresh_token:
                    return JsonResponse({'success': False, 'error': 'Refresh token révoqué'}, status=401)
                new_access_token = jwt.encode({'user_id': refresh_payload['user_id'], 'iat': int(time.time()), 'exp': int(time.time()) + 60 * 5}, settings.SECRET_KEY, algorithm='HS256')
                response = view_func(request, *args, **kwargs)
                response.set_cookie('token', new_access_token, max_age=60*5, httponly=True, secure=True, samesite='Strict')
                return response

            except ObjectDoesNotExist:
                return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)
            except jwt.ExpiredSignatureError:
                return JsonResponse({'success': False, 'error': 'Refresh token expiré'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'success': False, 'error': 'Refresh token invalide'}, status=400)
        return JsonResponse({'success': False, 'error': 'Accès refusé : jetons manquants ou expirés'}, status=401)

    return _wrapped_view


def jwt_42_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        access_token = request.COOKIES.get('42_access_token')

        if access_token:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url="https://api.intra.42.fr/oauth/token/info", headers=headers)
            token_data = response.json()
            expires_in_seconds = token_data.get('expires_in_seconds')

            intra_id = r.get(f'42_access_token_{access_token}')

            if expires_in_seconds is None or expires_in_seconds <= 0:
                return JsonResponse({'success': False, 'error': 'Access token 42 expire'}, status=400)

            if not intra_id:
                user_info_response = requests.get(url=os.getenv('USER_URL'), headers=headers)
                user_data = user_info_response.json()
                intra_id = user_data.get('id')
                user = User.objects.filter(custom_user__intra_id=intra_id).first()
                
            user = User.objects.filter(custom_user__intra_id=intra_id).first()
            # user = User.objects.filter(username=username).first()

            if not user:
                return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)
            redis_42_access_token = r.get(f'user_{user.custom_user.intra_id}_42_access_token')
            if redis_42_access_token and redis_42_access_token.decode() != access_token:
                return JsonResponse({'success': False, 'error': 'Access token 42 revoqué'}, status=401)
            request.user = user
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'success': False, 'error': 'Access token 42 manquand'}, status=400)

    return _wrapped_view


def request_from_42_or_regular_user(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.COOKIES.get('42_access_token'):
            return jwt_42_required(view_func)(request, *args, **kwargs)
        else:
            return jwt_required(view_func)(request, *args, **kwargs)
    
    return _wrapped_view

def twoFA_status_check(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        custom_user = CustomUser.objects.get(user=user) # custom_user = CustomUser.objects.get(user=user)  fonctionne, mais pas user.custom_user ou request.user.custom_user ???? why
        if custom_user.twoFA_enabled == False:
            return view_func(request, *args, **kwargs)
        twoFA_verified = r.get(f'user_{user.id}_twoFA_verified')
        if custom_user.twoFA_enabled and twoFA_verified and twoFA_verified.decode() == 'True':
            return view_func(request, *args, **kwargs)
        return JsonResponse({'Success': False, 'error': '2FA non verifié'}, status=401)
    
    return _wrapped_view
