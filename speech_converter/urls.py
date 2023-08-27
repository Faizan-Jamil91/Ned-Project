# speech_converter/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.convert_speech, name='convert_speech'),
]