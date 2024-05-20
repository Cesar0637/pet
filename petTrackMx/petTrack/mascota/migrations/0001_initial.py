# Generated by Django 4.0.10 on 2024-05-18 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300, verbose_name='Nombre de la mascota')),
                ('especie', models.CharField(blank=True, max_length=300, null=True, verbose_name='Especie')),
                ('raza', models.CharField(blank=True, max_length=300, null=True, verbose_name='Raza')),
                ('edad', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mascota_usuario', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]
