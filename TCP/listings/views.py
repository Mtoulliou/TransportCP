from django.http import HttpResponse
from django.shortcuts import render

def accueil(request):
    with open("pages/index.html", 'r') as file:
        html_content = file.read()
    return HttpResponse(html_content, content_type='text/html')