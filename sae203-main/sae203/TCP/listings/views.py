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
from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from .forms import ColisForm
from .models import colis, CustomUser, AdminTCP, Vehicle
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
import re
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login, logout     

def log_in(request): 
    if request.method =="POST":
        #print("ok2")
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        #print("ok3")
        user = CustomUser.objects.filter(email=email).first()
        #print("ok4")
        if user :
            #print("ok5")
            auth_user = authenticate(email=email, password=password)
            #print("ok6",email,password)
            if auth_user:
                #print("ok7")
                login(request, auth_user)
                #print(request.user.is_authenticated)
                #print(request.session.session_key)
                #Les prints servent de test en cas de problème
                return redirect('../accueil/')
            else:
                print("user pas auth")
        else: 
            print("no")


    return render(request, 'listings/log_in.html')     
    
def log_out(request):
    logout(request)
    return redirect('../log_in/')


def register(request): 
    error = False
    message = ""




    #Récupération des informations depuis le formulaire (une fois que le POST à était effectué)
    if request.method =="POST":
        nom = request.POST.get('nom', None)
        prenom = request.POST.get('prenom', None)
        adresse = request.POST.get('adresse', None)
        code_postal = request.POST.get('code_postal', None)
        ville = request.POST.get('ville', None)
        telephone = request.POST.get('telephone', None)
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

        # Vérification de la disponibilité de l'email
        user_with_email = CustomUser.objects.filter(email=email).first()

        if user_with_email:
            error = True
            message = f"L'email {email} est déjà associé à un compte. Veuillez utiliser une autre adresse e-mail."


        if error == False : 
            if password != password_confirm :
                error = True
                message = "Les deux mots de passe ne sont pas identiques ! " 
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
            user = CustomUser(
                nom=nom,
                prenom=prenom,
                adresse=adresse,
                code_postal=code_postal,
                ville=ville,
                telephone=telephone,
                email=email,
            )    
            user.save()
            user.password=password
            user.set_password(user.password)
            user.save()


            client_group = Group.objects.get(name='Client')  
            user.groups.add(client_group) 

            return redirect('../log_in/')

    
                


    context = {
        'error' : error,
        'message' : message
    }


    return render(request, 'listings/register.html', context)   
    




##################################################################
#######################   PAGES   ################################
##################################################################


def accueil(request):
    return render(request, 'listings/index.html')

def recherche_colis(request):
    if 'q' in request.GET:
        query = request.GET['q']
        coliss = colis.objects.filter(id__exact=query)
        return render(request, 'listings/recherche_colis.html', {'colis': coliss, 'query': query})
    else:
        return render(request, 'listings/recherche_colis.html')




@login_required(login_url='log_in_page')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists() or u.groups.filter(name='Admin').exists())
def destinataire(request):
    user = request.user
    coliss = colis.objects.filter(destinataire=user)
    return render(request, 'listings/destinataire.html',{'colis':coliss})

@login_required(login_url='log_in_page')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists() or u.groups.filter(name='Admin').exists())
def colis_recu(request):
    if request.method == 'POST':
        colis_id = request.POST.get('colis_id')
        coliss = colis.objects.get(id=colis_id)
        # Mettre à jour l'état du colis
        coliss.etat = colis.RECU
        coliss.save()
    
        return redirect('destinataire')
    else:
        return redirect('destinataire')




@login_required(login_url='log_in_page')
@user_passes_test(lambda u: u.groups.filter(name='Expediteur').exists() or u.groups.filter(name='Admin').exists())
def expediteur(request):
    if request.method == 'POST':
        form = ColisForm(request.POST)
        if form.is_valid():
            hauteur = form.cleaned_data['hauteur']
            largeur = form.cleaned_data['largeur']
            longueur = form.cleaned_data['longueur']
            poids = form.cleaned_data['poids']
            destination = form.cleaned_data['destination']
            destinataire = form.cleaned_data['destinataire']
            register = colis(hauteur=hauteur, largeur=largeur, longueur=longueur, poids=poids, destination=destination, destinataire=destinataire, expediteur=request.user.username)
            register.save()
            form = ColisForm()
            utilisateur_connecte = request.user
            coliss = colis.objects.filter(expediteur=utilisateur_connecte)
    else:
        form = ColisForm()
        utilisateur_connecte = request.user
        coliss = colis.objects.filter(expediteur=utilisateur_connecte)
    return render(request, 'listings/expediteur.html', {'form': form,'colis': coliss})

@login_required(login_url='log_in_page')
@user_passes_test(lambda u: u.groups.filter(name='Expediteur').exists() or u.groups.filter(name='Admin').exists())
def delete_colis(request, id):
    colis.objects.filter(id=id).delete()
    return HttpResponseRedirect('/expediteur')   




@login_required(login_url='log_in_page')
@user_passes_test(lambda u: u.groups.filter(name='Transporteur').exists() or u.groups.filter(name='Admin').exists())
def transporteur(request): 
    Vehicles = Vehicle.objects.all()
    return render(request, 'listings/transporteur.html', {'Vehicle': Vehicles})  

def attribuer_transporteur(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        # Récupérer l'utilisateur connecté
        transporteur = request.user
        # Récupérer le véhicule correspondant à l'ID
        vehicle = Vehicle.objects.get(id=vehicle_id)
        # Mettre à jour le champ transporteur du véhicule
        vehicle.transporteur = transporteur
        vehicle.save()
        return redirect('vehicule')
    else:
        return redirect('transporteur')

def vehicule(request):
    utilisateur_connecte = request.user
    rien=''
    coliss = colis.objects.filter(transporteur='Non affecté') | colis.objects.filter(transporteur=utilisateur_connecte)
    return render(request, 'listings/vehicule.html', {'colis': coliss})

def attribuer_colis(request):
    if request.method == 'POST':
        colis_id = request.POST.get('colis_id')
        
        # Récupérer l'utilisateur connecté
        user = request.user
        
        # Récupérer le colis correspondant à l'ID
        coliss = colis.objects.get(id=colis_id)
        
        # Mettre à jour le champ transporteur du colis avec le nom de l'utilisateur
        coliss.transporteur = user.username
        
        # Enregistrer les modifications
        coliss.save()
        
        return redirect('vehicule')
    else:
        return redirect('vehicule')
    
def colis_arrive(request):
    if request.method == 'POST':
        colis_id = request.POST.get('colis_id')
        coliss = colis.objects.get(id=colis_id)
        # Mettre à jour l'état du colis
        coliss.etat = colis.ARRIVEE
        coliss.save()
    
        return redirect('vehicule')
    else:
        return redirect('vehicule')
    
def colis_depart(request):
    if request.method == 'POST':
        colis_id = request.POST.get('colis_id')
        coliss = colis.objects.get(id=colis_id)
        # Mettre à jour l'état du colis
        coliss.etat = colis.DEPART
        coliss.save()
    
        return redirect('vehicule')
    else:
        return redirect('vehicule')
    
def colis_livre(request):
    if request.method == 'POST':
        colis_id = request.POST.get('colis_id')
        coliss = colis.objects.get(id=colis_id)
        # Mettre à jour l'état du colis
        coliss.etat = colis.LIVRE
        coliss.save()
    
        return redirect('vehicule')
    else:
        return redirect('vehicule')
