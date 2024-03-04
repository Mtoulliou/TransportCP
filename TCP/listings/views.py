from django.http import HttpResponse
from django.shortcuts import render
from listings.models import AdminTCP

def accueil(request):
    admintcp=AdminTCP.objects.all()
    return render(request, 'listings/index.html',{'admintcp':admintcp})