# Generated by Django 5.1 on 2024-08-25 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Historia', '0003_alter_efaparato_pulso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='apellidos',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='direccion',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]
