# Generated by Django 2.0.1 on 2018-05-04 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airlineapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='reference_number',
            field=models.CharField(default='unknown', max_length=20),
        ),
    ]