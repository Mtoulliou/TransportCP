"""

Nom ......... : urls.py
Role ........ : récupère l'url du navigateur et redirige vers la fonction voulu dabs le fichier views.py.
                
Auteur ...... : Nathan Renieville & Mattéo Toulliou
Version ..... : V1.0 du 06/04/2024

Contact : nathan.renieville@etu.umontpellier.fr
          matteo.toulliou@etu.umontpellier.fr
"""


"""
URL configuration for TCP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from listings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil),
    path('accueil/', views.accueil),
    path('expediteur/', views.expediteur),
    path('expediteur/supprimer/<int:colis_id>/', views.supprimer_colis, name='supprimer_colis'),
    path('destinataire/', views.destinataire),
    path('transporteur/', views.transporteur),
    path('recherche/', views.recherche_colis, name='recherche_colis'),
    path('register/', views.register),
    path('log_in/', views.log_in, name='log_in_page'),
]
