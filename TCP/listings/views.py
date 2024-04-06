"""

Nom ......... : views.py
Role ........ : Affiche les pages demandés par l'utilisateur, 
                intéragis avec les pages, notamment pour l'inscription Register.html
                
Auteur ...... : Nathan Renieville & Mattéo Toulliou

Version ..... : V1.1 du 15/03/2024 : ajout des pages expediteur, destinataire, transporteur
                V1.2 du 20/03/2024 : ajout des pages recherche_colis et supprimer_colis
                V1.3 du 06/04/2024 : ajout de la partie register et log_in

Contact : nathan.renieville@etu.umontpellier.fr
          matteo.toulliou@etu.umontpellier.fr
"""



from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from listings.models import AdminTCP,Colis
from listings.form import ColisForm
from django.shortcuts import render, redirect
from .models import Colis
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout     

def log_in(request): 
    if request.method =="POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)


        user = User.objects.filter(email=email).first()
        if user :
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('../accueil/')

            else:
                print("user pas auth")
        else: 
            print("no")


    return render(request, 'listings/log_in.html')   
    



def register(request): 
    error = False
    message = ""

    #Récupération des informations depuis le formulaire (une fois que le POST à était effectué)
    if request.method =="POST":
        name = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password_confirm = request.POST.get('password_confirm', None)
        
        #Vérification de la validité de l'email
        try:
            validate_email(email)
            print(error)
        except ValidationError:
            error = True
            message = f"L'email {email} n'est pas valide."
            print(error)

        #Vérification de la disponibilité du nom avec l'email renseigné.
        user= User.objects.filter(Q (email=email) | Q(username=name)).first()
        if user :
            error = True
            message = f"Nom d'utilisateur indisponible avec l'email {email} ou le nom d'utilisateur {name} existe déjà."


        if error == False : 
            if password != password_confirm :
                error = True
                message = "Les deux mots de passe sont identiques ! " 
            #Vérification taille du mot de passe
            if len(password) < 8:
                error = True
                message = "Le mot de passe doit contenir au moins 5 caractères."
            #Vérification si symboles, chiffres, lettre majuscules et minuscules.
            if not re.search(r'[\W_]', password):
                error = True
                message = "Le mot de passe doit contenir au moins un symbole."
            elif not re.search(r'[A-Z]', password):
                error = True
                message = "Le mot de passe doit contenir au moins une majuscule."
            elif not re.search(r'[a-z]', password):
                error = True
                message = "Le mot de passe doit contenir au moins une minuscule."
            elif not re.search(r'\d', password):
                error = True
                message = "Le mot de passe doit contenir au moins un chiffre."
        
        if error == False :     
            user = User(
                username=name,
                email=email,

            )    
            user.save()
            user.password=password
            user.set_password(user.password)
            user.save()
            return redirect('../log_in/')

    
                


    context = {
        'error' : error,
        'message' : message
    }


    return render(request, 'listings/register.html', context)   
    


@login_required(login_url='log_in_page')
def recherche_colis(request):
    if 'q' in request.GET:
        query = request.GET['q']
        colis = Colis.objects.filter(numeroSuivi__exact=query)
        return render(request, 'listings/recherche_colis.html', {'colis': colis, 'query': query})
    else:
        return render(request, 'listings/recherche_colis.html')

@login_required(login_url='log_in_page')
def accueil(request):
    admintcp=AdminTCP.objects.all()
    return render(request, 'listings/index.html',{'admintcp':admintcp})

@login_required(login_url='log_in_page')
def destinataire(request):
    return render(request, 'listings/destinataire.html')

@login_required(login_url='log_in_page')
def expediteur(request):
    colis=Colis.objects.all()
    form = ColisForm(request.POST or None)
    if form.is_valid() : 
        form.save()
    return render(request, 'listings/expediteur.html',{'colis':colis, 'form':form})

@login_required(login_url='log_in_page')
def supprimer_colis(request, colis_id):
    colis = get_object_or_404(Colis, pk=colis_id)
    colis.delete()
    return (request, 'listings/expediteur.html')     

@login_required(login_url='log_in_page')
def transporteur(request): 
    return render(request, 'listings/transporteur.html')  


        
