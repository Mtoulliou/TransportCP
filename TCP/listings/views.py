from django.http import HttpResponse
from django.shortcuts import render
from listings.models import AdminTCP,Colis
from listings.form import ColisForm

def accueil(request):
    admintcp=AdminTCP.objects.all()
    return render(request, 'listings/index.html',{'admintcp':admintcp})

def destinataire(request):
    return render(request, 'listings/destinataire.html')

def expediteur(request):
    colis=Colis.objects.all()
    form = ColisForm(request.POST or None)
    if form.is_valid() : 
        form.save()
    return render(request, 'listings/expediteur.html',{'colis':colis, 'form':form})      

def transporteur(request): 
    return render(request, 'listings/transporteur.html')    