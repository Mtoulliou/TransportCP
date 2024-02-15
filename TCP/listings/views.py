from django.http import HttpResponse
from django.shortcuts import render
from listings.models import AdminTCP

def accueil(request):
    AdminTCP = AdminTCP.objects.all()
    with open("pages/index.html", 'r') as file:
        html_content = file.read()
    return HttpResponse(html_content, content_type='text/html')