# Generated by Django 5.1 on 2024-08-31 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Historia', '0007_alter_paciente_direccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='efaparato',
            name='indice_corporal',
            field=models.FloatField(),
        ),
    ]
