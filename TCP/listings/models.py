from django.db import models
import random
from django.core.validators import MaxValueValidator,MinValueValidator

class Colis(models.Model):
    EMBALLE = 'EMBALLE'
    ARRIVEE = 'ARRIVEE'
    DEPART = 'DEPART'
    LIVRE = 'LIVRE'
    RECU = 'RECU'

    AUCUNE = 'AUCUNE'
    MAIL = 'MAIL'
    CODE = 'CODE'


    ETAT_CHOICES = [
        (EMBALLE, 'Emballé'),
        (ARRIVEE, 'Arrivée'),
        (DEPART, 'Départ'),
        (LIVRE, 'Livré'),
        (RECU, 'Reçu')
    ]

    CONFIRMATION_CHOICES = [
        (AUCUNE, 'Aucune'),
        (MAIL, 'Mail'),
        (CODE, 'Code')
    ]

    numeroSuivi = models.AutoField(primary_key=True)
    poids = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(999999999.99)])
    longueur = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(999999999.99)])
    largeur = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(999999999.99)])
    hauteur = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(999999999.99)])
    etat = models.CharField(max_length=10,choices=ETAT_CHOICES,default=EMBALLE)
    expediteur = models.ForeignKey('Expediteur', on_delete=models.CASCADE)
    destinataire = models.ForeignKey('Destinataire', on_delete=models.CASCADE)
    vehicule = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    adresseLivraison = models.CharField(max_length=255)
    typeDeConfirmation = models.CharField(max_length=10,choices=CONFIRMATION_CHOICES)
    numeroConfirmation = models.CharField(max_length=6)

    #def save(self, *args, **kwargs):
    #    if not self.numeroConfirmation:  # Générer un code de confirmation uniquement s'il n'est pas déjà défini
    #        self.numeroConfirmation = ''.join(random.choices('0123456789', k=6))  # Générer un code à 6 chiffres
    #    super(Colis, self).save(*args, **kwargs)  # Appeler la méthode save() du modèle parent

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE)
    localisation = models.CharField(max_length=255)

class Expediteur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    mdp = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    codePostal = models.CharField(max_length=5)
    ville = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    tel = models.CharField(max_length=10)

class Transporteur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    mdp = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    codePostal = models.CharField(max_length=5)
    ville = models.CharField(max_length=100)
    mail = models.EmailField(max_length=10)
    tel = models.CharField(max_length=10)

class Destinataire(models.Model):
    id = models.AutoField(primary_key=True)
    
    nom = models.CharField(max_length=100)
    mdp = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    codePostal = models.CharField(max_length=5)
    ville = models.CharField(max_length=100)
    mail = models.EmailField(max_length=10)
    tel = models.CharField(max_length=10)

class AdminTCP(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    mdp = models.CharField(max_length=100)

