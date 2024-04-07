from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings





class colis(models.Model):
    EMBALLE = 'EMBALLE'
    ARRIVEE = 'ARRIVEE'
    DEPART = 'DEPART'
    LIVRE = 'LIVRE'
    RECU = 'RECU'

    ETAT_CHOICES = [
        (EMBALLE, 'Emballé'),
        (ARRIVEE, 'Arrivée'),
        (DEPART, 'Départ'),
        (LIVRE, 'Livré'),
        (RECU, 'Reçu')
    ]

    id = models.AutoField(primary_key=True)
    hauteur = models.CharField(max_length=100)
    largeur = models.CharField(max_length=100)
    longueur = models.CharField(max_length=100)
    poids = models.FloatField(max_length=100)
    destination = models.CharField(max_length=100)
    etat = models.CharField(max_length=10, choices=ETAT_CHOICES, default=EMBALLE)
    expediteur = models.CharField(max_length=100)
    transporteur = models.CharField(max_length=100, default='Non affecté')
    destinataire = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"Colis {self.id} - {self.etat}"

    @classmethod
    def recherche_par_numero(cls, numero):
        return cls.objects.filter(id=numero)
    

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    transporteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    localisation = models.CharField(max_length=255)






class CustomUser(AbstractUser):

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


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
        """
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

    """
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



