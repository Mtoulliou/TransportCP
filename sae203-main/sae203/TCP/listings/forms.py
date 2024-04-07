from django.core import validators
from django import forms
from .models import colis

class ColisForm(forms.ModelForm):
    class Meta:
        model = colis
        fields = ['hauteur','largeur','longueur','poids','destination','destinataire']
        widgets = {
            'hauteur': forms.TextInput(attrs={'class': 'form-control'}),
            'largeur': forms.TextInput(attrs={'class': 'form-control'}),
            'longueur': forms.TextInput(attrs={'class': 'form-control'}),
            'poids': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'destinataire': forms.TextInput(attrs={'class': 'form-control'}),

        }