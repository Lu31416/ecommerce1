from django.urls import path
from base.views import inicio

urlpatterns = [
    path('', inicio, name='home'),
]

from django.shortcuts import render

def inicio(request):
    return render(request, 'inicio.html')