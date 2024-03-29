# Generated by Django 2.0.1 on 2018-05-04 01:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aircraft_type', models.CharField(default='unspecified', max_length=20)),
                ('aircraft_registration_number', models.CharField(max_length=10, unique=True)),
                ('aircraft_number_seats', models.IntegerField(default='unspecified')),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airport_name', models.CharField(max_length=50, unique=True)),
                ('airport_country', models.CharField(default='unspecified', max_length=50)),
                ('airport_time_zone', models.CharField(default='unspecified', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_number', models.CharField(max_length=10, unique=True)),
                ('booked_seats', models.IntegerField(default='unspecified')),
                ('booking_status', models.CharField(default='ON_HOLD', max_length=10)),
                ('time_to_complete', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_num', models.CharField(default='unspecified', max_length=10)),
                ('dep_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('arr_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('duration', models.DurationField(default=0)),
                ('price', models.FloatField(default=0)),
                ('aircraft_type', models.ForeignKey(null='True', on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Aircraft')),
                ('dep_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dep_airport', to='airlineapp.Airport')),
                ('dest_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dest_airport', to='airlineapp.Airport')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.CharField(default='unknown', max_length=20, unique=True)),
                ('amount', models.FloatField(default='unspecified')),
                ('paid', models.BooleanField(default=False)),
                ('stamp', models.CharField(default='', max_length=10)),
                ('booking_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Booking')),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='unspecified', max_length=50)),
                ('surname', models.CharField(default='unspecified', max_length=50)),
                ('email', models.EmailField(default='unspecified@unspecified.com', max_length=50)),
                ('phone', models.CharField(default='unspecified', max_length=15)),
                ('booking_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Booking')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unspecified', max_length=50)),
                ('website', models.URLField(default='unspecfied')),
                ('account_number', models.CharField(default='unspecified', max_length=50)),
                ('login_name', models.CharField(default='unspecified', max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_flight',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airlineapp.Flight'),
        ),
    ]
