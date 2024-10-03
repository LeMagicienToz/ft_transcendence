from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.receive_user, name='receive_user'),
]
