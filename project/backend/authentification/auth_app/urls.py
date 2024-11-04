from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('login/42/', views.login_42, name='login_42'),
    path('callback/42/', views.callback_42, name='callback_42'),
	path('reset_password/', views.reset_password, name='reset_password'),
	path('delete_account/', views.delete_account, name='delete_account'),
    path('get_user/', views.get_user, name='get_user'),
    path('set_user_color/', views.set_user_color, name='set_user_color'),
    path('set_profile/', views.set_profile, name='set_profile'),
    path('twoFA_validation/', views.twoFA_validation, name='twoFA_validation'),
    path('search_user/', views.search_user, name='search_user'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('remove_friend/', views.remove_friend, name='remove_friend'),
    path('get_friends_list/', views.get_friends_list, name='get_friends_list'),
]
