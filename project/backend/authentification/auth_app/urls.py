from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('login/42/', views.login_42, name='login_42'),
    path('callback/42/', views.callback_42, name='callback_42'),
	path('reset_password/', views.reset_password, name='reset_password'),
	path('delete_account/', views.delete_account, name='delete_account'),
]
