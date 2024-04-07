from django.contrib import admin
from .models import CustomUser,colis, Vehicle, Transporteur
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

admin.site.register(CustomUser)



class CustomGroupAdmin(GroupAdmin):
    admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)

@admin.register(colis)
class ColisAdmin(admin.ModelAdmin):
    list_display = ('id','hauteur','largeur','longueur','poids','destination','etat','expediteur','transporteur','destinataire')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id','transporteur','localisation')

@admin.register(Transporteur)
class TransporteurAdmin(admin.ModelAdmin):
    list_display = ('id','nom','mdp','adresse','codePostal','ville','mail','tel')