from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path('autocadastro/', views.autocadastro, name='autocadastro'),
]

