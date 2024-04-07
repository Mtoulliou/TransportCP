from django.http import HttpResponse
from django.shortcuts import render
from listings.models import AdminTCP

def accueil(request):
    admintcp=AdminTCP.objects.all()
    return render(request, 'listings/index.html',{'admintcp':admintcp})

def destinataire(request):
    return render(request, 'listings/destinataire.html')

def expediteur(request):
    return render(request, 'listings/expediteur.html')      

def transporteur(request): 
    return render(request, 'listings/transporteur.html')    