# Generated by Django 4.1.13 on 2024-01-31 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appAPI1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='marca',
            field=models.ForeignKey(choices=[('Audi', 'Audi'), ('BMW', 'BMW'), ('Renault', 'Renault')], on_delete=django.db.models.deletion.CASCADE, to='appAPI1.marca'),
        ),
    ]
