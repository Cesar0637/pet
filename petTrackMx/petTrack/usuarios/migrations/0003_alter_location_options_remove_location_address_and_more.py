# Generated by Django 4.0.10 on 2024-05-18 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['id'], 'verbose_name': 'Ubicación', 'verbose_name_plural': 'Ubicaciones'},
        ),
        migrations.RemoveField(
            model_name='location',
            name='address',
        ),
        migrations.RemoveField(
            model_name='location',
            name='name',
        ),
    ]
