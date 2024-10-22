import jwt
from django.conf import settings
from django.http import JsonResponse

def jwt_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        access_token = request.COOKIES.get('token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                request.user_id = payload['user_id']
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
            request.access_token_42 = access_token
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'Access token 42 manquand'}, status=401)
