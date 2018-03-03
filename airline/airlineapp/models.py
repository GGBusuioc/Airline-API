from django.db import models

# Create your models here.

class Aircraft(models.Model):
    # aircraft type (e.g. Airbus A320)
    aircraft_type = models.CharField(max_length=20, default="unspecified")
    # unique tail or registration number (e.g. G-STBA)
    aircraft_registration_number = models.CharField(max_length=10, unique=True)
    # number of seats (e.g. 150)
    aircraft_number_seats = models.IntegerField(default="unspecified")

class Airport(models.Model):
    # airport unique name (e.g. New York JFK)
    airport_name = models.CharField(max_length=50, unique=True)
    # country (e.g. USA)
    airport_country = models.CharField(max_length=50, default="unspecified")
    # time zone of the airport (e.g. 'USA EASTERN EST')
    airport_time_zone = models.CharField(max_length=50, default="unspecified")

class Flight(models.Model):
    # flight number (e.g. BA1349)
    flight_number = models.CharField(max_length=10, default="unspecified")
    # departue airport (e.g. London Heathrow LHR)
    departue_airport = models.CharField(max_length=50, default="unspecified")
    # destination airport (e.g. New York JFK)
    destination_airport = models.CharField(max_length=50, default="unspecified")
    # departure date-time (e.g. 2018.04.01, 14:45:00)
    # departue_datetime = models.DateTimeField(default="unspecified")
    # # arrival date-time (e.g. 2018.04.01, 20:30:00)
    # arrival_datetime = models.DateTimeField(default="unspecified")
    #  flight duration (e.g. 5:15:00, i.e. 5 hours and 15 minutes)
    #duration = models.DurationField(default="unspecified")

    # aircraft type used for this flight (a foreign key to aircraft table)
    #aircraft_type = models.ForeignKey('Aircraft', on_delete=models.CASCADE)

    # price of a single seat on this Flight
    #ticket_price = models.FloatField(default="unspecified")

    def __str__(self):
        return ("%s" % (self.flight_number))



class Booking(models.Model):
    # unique booking number (e.g. WXY12Z)
    booking_number = models.CharField(max_length=10, unique=True)
    # flight associated with this booking (a foreign key to the flights table)
    booking_flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    # number of seats booked.
    booking_seats_number = models.IntegerField(default="unspecified")
    # passengers
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE)
    # status of this booking (ONHOLD, CONFIRMED, CANCELLED, or TRAVELLED)
    STATUS_CHOICES = (('ONHOLD', 'ONHOLD'), ('CONFIRMED','CONFIRMED'), ('CANCELLED', 'CANCELLED'), ('TRAVELLED','TRAVELLED'))
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='ONHOLD')
    #  time this booking will no longer be valid if the status of the booking is ONHOLD.
    time_to_complete = models.TimeField(default="unspecified")

class Passenger(models.Model):
    # details of each passenger  (first name, surname, email, and phone number).
    firstname = models.CharField(max_length=50, default="unspecified")
    surname = models.CharField(max_length=50, default="unspecified")
    email = models.EmailField(max_length=50, default="unspecified@unspecified.com")
    phone_number = models.CharField(max_length=15, default="unspecified")

class PaymentProvider(models.Model):
    # name of the payment service provider (e.g. SalPay)
    name = models.CharField(max_length=50, default="unspecified")
    # address of the website of the payment service provider (e.g. ‘www. salpay.co.uk’)
    website = models.URLField(max_length=200, default="unspecfied")
    # accout number
    account_number = models.CharField(max_length=50, default="unspecified")
    # login name and password (this is needed when the airline server must access their
    # account to create an electronic invoice for a customer)
    login_name = models.CharField(max_length=50, default="unspecified")
    password = models.CharField(max_length=50, null=False)

class Invoice(models.Model):
    #  unique reference number for this invoice at the airline’s database
    reference_number = models.CharField(max_length=10, unique=True)
    # unique reference number for this invoice within the database of the payment service provider

    #  booking number for which the invoice was issued.
    booking_number = models.ForeignKey('Booking', on_delete=models.CASCADE)
    #  amount of the invoice
    ammount = models.FloatField(default="unspecified")
    # paid or not
    paid = models.BooleanField(default=False)
    # electronic stamp (10 autogenerated digit alphanumeric )
