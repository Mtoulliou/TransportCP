# Generated by Django 5.0.2 on 2024-03-05 09:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colis',
            name='destinataire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='listings.destinataire'),
        ),
        migrations.AlterField(
            model_name='colis',
            name='expediteur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='listings.expediteur'),
        ),
        migrations.AlterField(
            model_name='colis',
            name='numeroConfirmation',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='colis',
            name='vehicule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='listings.vehicle'),
        ),
    ]
