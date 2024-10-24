import jwt
import requests
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
import os

def jwt_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        access_token = request.COOKIES.get('token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                try:
                    request.user = User.objects.get(id=payload['user_id'])
                except User.DoesNotExist:
                    return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
                return view_func(request, *args, **kwargs)

            except jwt.ExpiredSignatureError:
                if refresh_token:
                    try:
                        refresh_payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
                        new_access_token = jwt.encode({'user_id': refresh_payload['user_id'], 'iat': int(time.time()), 'exp': int(time.time()) + 60 * 5}, settings.SECRET_KEY, algorithm='HS256')
                        response = view_func(request, *args, **kwargs)
                        response.set_cookie('token', new_access_token, max_age=60*5, httponly=True, secure=True, samesite='Strict')
                        return response
                        
                    except jwt.ExpiredSignatureError:
                        return JsonResponse({'error': 'Refresh token expire'}, status=401)
                    except jwt.InvalidTokenError:
                        return JsonResponse({'error': 'Refresh token invalide'}, status=401)
                else:
                    return JsonResponse({'error': 'Access token expire and refresh token manquand'}, status=401)

            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Token invalide'}, status=401)
        else:
            return JsonResponse({'error': 'Access token manquand'}, status=401)

    return _wrapped_view


def jwt_42_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        access_token = request.COOKIES.get('42_access_token')

        if access_token:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url="https://api.intra.42.fr/oauth/token/info", headers=headers)
            token_data = response.json()
            expires_in_seconds = token_data.get('expires_in_seconds')

            if expires_in_seconds is None or expires_in_seconds <= 0:
                return JsonResponse({'success': False, 'error': 'Access token 42 expire'}, status=400)

            user_info_response = requests.get(url=os.getenv('USER_URL'), headers=headers)
            user_data = user_info_response.json()
            username = user_data.get('login') + '#42'
            user = User.objects.filter(username=username).first()

            if not user:
                return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)

            request.user = user
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'Access token 42 manquand'}, status=401)

    return _wrapped_view


def request_from_42_or_regular_user(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.COOKIES.get('42_access_token'):
            return jwt_42_required(view_func)(request, *args, **kwargs)
        else:
            return jwt_required(view_func)(request, *args, **kwargs)
    
    return _wrapped_view
