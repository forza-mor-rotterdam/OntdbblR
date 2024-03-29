# Generated by Django 3.2.16 on 2024-01-19 11:51

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Permissie",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "permissions": [
                    ("gebruiker_lijst_bekijken", "Gebruiker lijst bekijken"),
                    ("gebruiker_aanmaken", "Gebruiker aanmaken"),
                    ("gebruiker_aanpassen", "Gebruiker aanpassen"),
                    ("gebruiker_bekijken", "Gebruiker bekijken"),
                    ("gebruiker_verwijderen", "Gebruiker verwijderen"),
                    ("beheer_bekijken", "Beheer bekijken"),
                    ("context_lijst_bekijken", "Rol lijst bekijken"),
                    ("context_aanmaken", "Rol aanmaken"),
                    ("context_bekijken", "Rol bekijken"),
                    ("context_aanpassen", "Rol aanpassen"),
                    ("context_verwijderen", "Context verwijderen"),
                    ("rechtengroep_lijst_bekijken", "Rechtengroep lijst bekijken"),
                    ("rechtengroep_aanmaken", "Rechtengroep aanmaken"),
                    ("rechtengroep_bekijken", "Rechtengroep bekijken"),
                    ("rechtengroep_aanpassen", "Rechtengroep aanpassen"),
                    ("rechtengroep_verwijderen", "Rechtengroep verwijderen"),
                ],
                "managed": False,
                "default_permissions": (),
            },
        ),
    ]
