# Generated by Django 2.0.1 on 2018-05-04 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airlineapp', '0002_auto_20180504_0647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='reference_number',
        ),
    ]