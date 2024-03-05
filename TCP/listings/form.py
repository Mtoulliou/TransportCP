from django import forms
from .models import Colis

class ColisForm(forms.ModelForm):
    model = Colis
    fields = ['poids', 'longueur', 'largeur', 'hauteur', 'destinataire', 'adresseLivraison', 'typeDeConfirmation']