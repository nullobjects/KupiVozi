from django.urls import path
from . import views

urlpatterns = [
    path('api/set-csrf-token', views.set_csrf_token, name='set_csrf_token'),
]