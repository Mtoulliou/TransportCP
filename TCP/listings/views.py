from django.http import HttpResponse
from django.shortcuts import render

def accueil(request):
    return HttpResponse('<h1>TCP</h1>\n<h2>Transport Colis Passion</h2>')