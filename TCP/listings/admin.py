from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

admin.site.register(CustomUser)



class CustomGroupAdmin(GroupAdmin):
    admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)


