# Generated by Django 2.0.1 on 2018-03-08 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airlineapp', '0002_auto_20180308_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='booking_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Booking'),
        ),
    ]