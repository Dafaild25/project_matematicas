# Generated by Django 5.0.6 on 2025-06-16 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_administradores_adm_fotografia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personas',
            name='per_edad',
        ),
    ]
