from django.db import models
import random
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser



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
    etat = models.CharField(max_length=10, choices=ETAT_CHOICES, default=EMBALLE)
    expediteur = models.ForeignKey('Expediteur', on_delete=models.CASCADE, default=None, null=True)
    destinataire = models.ForeignKey('Destinataire', on_delete=models.CASCADE, default=None, null=True)
    vehicule = models.ForeignKey('Vehicle', on_delete=models.CASCADE, default=None, null=True, blank=True)
    adresseLivraison = models.CharField(max_length=255)
    typeDeConfirmation = models.CharField(max_length=10, choices=CONFIRMATION_CHOICES)
    numeroConfirmation = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f"Colis {self.numeroSuivi} - Poids: {self.poids} kg - État: {self.etat}"
    
    @classmethod
    def recherche_par_numero(cls, numero):
        return cls.objects.filter(numeroSuivi=numero)
    
    def save(self, *args, **kwargs):
        if not self.numeroConfirmation:
            self.numeroConfirmation = str(random.randint(100000, 999999))
        super().save(*args, **kwargs) 
    

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    transporteur = models.ForeignKey('Transporteur', on_delete=models.CASCADE)
    localisation = models.CharField(max_length=255)






class CustomUser(AbstractUser):

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'


    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    code_postal = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, default='')

    def generate_default_username(self):
        return f"{self.nom}_{self.prenom}"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_default_username()
        super().save(*args, **kwargs)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Changement de related_name pour éviter le conflit
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Changement de related_name pour éviter le conflit
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username











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
    mail = models.EmailField(max_length=100) 
    tel = models.CharField(max_length=10)

class Destinataire(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    mdp = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    codePostal = models.CharField(max_length=5)
    ville = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100) 
    tel = models.CharField(max_length=10)

class AdminTCP(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    mdp = models.CharField(max_length=100)



