from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from .models import CustomUser

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
                            not all(c in '0123456789ABCDEF' for c in color_value[1:])):
            return JsonResponse({'success': False, 'error': f'Couleur {color_name} invalide'}, status=400)

    try:
        user.custom_user.suitColor = suitColor
        user.custom_user.visColor = visColor
        user.custom_user.ringsColor = ringsColor
        user.custom_user.bpColor = bpColor
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)
    return JsonResponse({'success': True, 'message': 'Couleurs mises à jour avec succès', 'user_id': user.id}, status=200)


def utils_set_username(data, user): # la fonction ne save pas l'objet user
    username = data.get('username')
    if username and (username.endswith('#42') or '@' in username):
        return JsonResponse({'success': False, 'error': 'Nom d\'utilisateur invalide'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'error': 'Nom d\'utilisateur déjà utilisé'}, status=400)
    user.username = data.get('username')
    return JsonResponse({'success': True, 'message': 'Nom d\'utilisateur valide'}, status=200)

def utils_set_email(data, user): # la fonction ne save pas l'objet user
    email = data.get('email')
    if email and (email.endswith('@student.42.fr') or not '@' in email):
        return JsonResponse({'success': False, 'error': 'Email invalide'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'error': 'Email déjà utilisé'}, status=400)
    user.email = data.get('email')
    return JsonResponse({'success': True, 'message': 'Email valide'}, status=200)