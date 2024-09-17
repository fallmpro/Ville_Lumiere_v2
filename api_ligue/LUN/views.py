
from django.http import HttpResponse
from django.shortcuts import render
import requests

# Vue pour la page principale
def home(request):
    return render(request, 'home.html')