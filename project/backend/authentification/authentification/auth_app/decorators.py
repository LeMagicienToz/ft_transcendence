import jwt
from django.conf import settings
from django.http import JsonResponse

def jwt_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        refresh_token = request.COOKIES.get('refresh_token')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, settings.DJANGO_SECRET_KEY, algorithms=['HS256'])
                request.user_id = payload['user_id']
                return view_func(request, *args, **kwargs) # token valide on traite la requete
            except jwt.ExpiredSignatureError:
                if refresh_token:
                    try:
                        refresh_payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
                        new_access_token = jwt.encode({'user_id': refresh_payload['user_id'], 'iat': int(time.time()), 'exp': int(time.time()) + 60 * 5}, settings.DJANGO_SECRET_KEY, algorithm='HS256')
                        response = view_func(request, *args, **kwargs)
                        
                        response_data = {
                            'message': 'Requête traitée avec succès',
                            'new_access_token': new_access_token,
                            **response.data
                        }
                        return JsonResponse(response_data)
                        
                    except jwt.ExpiredSignatureError:
                        return JsonResponse({'error': 'Refresh token expiré, veuillez vous reconnecter'}, status=401)
                    except jwt.InvalidTokenError:
                        return JsonResponse({'error': 'Refresh token invalide, veuillez vous reconnecter'}, status=401)
                else:
                    return JsonResponse({'error': 'Token expiré et refresh token manquant, veuillez vous reconnecter'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Token invalide, veuillez vous reconnecter'}, status=401)

        return JsonResponse({'error': 'Token manquant ou mal formé'}, status=401)

    return _wrapped_view