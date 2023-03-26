# Generated by Django 3.1.2 on 2023-03-28 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0007_adven_ticket_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adven_booking',
            name='check_in_day',
            field=models.ManyToManyField(related_name='adven_day', to='flight.Week'),
        ),
        migrations.AlterField(
            model_name='adven_booking',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival', to='flight.adven_place'),
        ),
        migrations.AlterField(
            model_name='adven_booking',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depart', to='flight.adven_place'),
        ),
    ]