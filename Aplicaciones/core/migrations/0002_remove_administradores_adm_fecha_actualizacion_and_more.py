# Generated by Django 5.0.6 on 2025-06-16 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administradores',
            name='adm_fecha_actualizacion',
        ),
        migrations.RemoveField(
            model_name='docentes',
            name='doc_fecha_actualizacion',
        ),
        migrations.RemoveField(
            model_name='estudiantes',
            name='est_fecha_actualizacion',
        ),
    ]
