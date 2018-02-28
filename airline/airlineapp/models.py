from django.db import models

# Create your models here.

class Aircraft(models.Model):
    # aircraft type (e.g. Airbus A320)
    aircraft_type = models.CharField(max_length=20)
    # unique tail or registration number (e.g. G-STBA)
    registration_number = models.CharField(max_length=10, unique=True)
    # number of seats (e.g. 150)
    number_seats = models.IntegerField(max_length=10)

class Airport(models.Model):
    # airport unique name (e.g. New York JFK)
    name = models.CharField(max_length=50, unique=True)
    # country (e.g. USA)
    country = models.CharField(max_length=50)
    # time zone of the airport (e.g. 'USA EASTERN EST')
    time_zone = models.CharField(max_length=50)

class Flight(models.Model):
    # flight number (e.g. BA1349)

    # departue airport (e.g. London Heathrow LHR)

    # destination airport (e.g. New York JFK)

    # departure date-time (e.g. 2018.04.01, 14:45:00)

    # arrival date-time (e.g. 2018.04.01, 20:30:00)

    # arrival date-time (e.g. 2018.04.01, 20:30:00)

    # aircraft type used for this flight (a foreign key to aircraft table)

    # price of a single seat on this Flight

class Booking(models.Model):
    # unique booking number (e.g. WXY12Z)

    # flight associated with this booking (a foreign key to the flights table)

    # number of seats booked.

    # details of each passenger  (first name, surname, email, and phone number).

    # status of this booking (ONHOLD, CONFIRMED, CANCELLED, or TRAVELLED)

    #  time this booking will no longer be valid if the status of the booking is ONHOLD.


class PaymentProvide(models.Model):
    # name of the payment service provider (e.g. SalPay)

    # address of the website of the payment service provider (e.g. ‘www. salpay.co.uk’)

    # accout number

    # login name and password (this is needed when the airline server must access their
    # account to create an electronic invoice for a customer)


class Invoice(models.Model):
    # ?
