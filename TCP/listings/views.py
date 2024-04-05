from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from listings.models import AdminTCP,Colis
from listings.form import ColisForm
from django.shortcuts import render
from .models import Colis

def recherche_colis(request):
    if 'q' in request.GET:
        query = request.GET['q']
        colis = Colis.objects.filter(numeroSuivi__exact=query)
        return render(request, 'listings/recherche_colis.html', {'colis': colis, 'query': query})
    else:
        return render(request, 'listings/recherche_colis.html')

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

def supprimer_colis(request, colis_id):
    colis = get_object_or_404(Colis, pk=colis_id)
    colis.delete()
    return (request, 'listings/expediteur.html')     

def transporteur(request): 
    return render(request, 'listings/transporteur.html')    