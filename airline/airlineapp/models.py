from django.db import models
from django.utils import timezone
class Aircraft(models.Model):
    # aircraft type (e.g. Airbus A320)
    aircraft_type = models.CharField(max_length=20, default="unspecified")
    # unique tail or registration number (e.g. G-STBA)
    aircraft_registration_number = models.CharField(max_length=10, unique=True)
    # number of seats (e.g. 150)
    aircraft_number_seats = models.IntegerField(default="unspecified")

    def __str__(self):
        return ("%s" % (self.aircraft_type))

class Airport(models.Model):
    # airport unique name (e.g. New York JFK)
    airport_name = models.CharField(max_length=50, unique=True)
    # country (e.g. USA)
    airport_country = models.CharField(max_length=50, default="unspecified")
    # time zone of the airport (e.g. 'USA EASTERN EST')
    airport_time_zone = models.CharField(max_length=50, default="unspecified")
    def __str__(self):
        return ("%s" % (self.airport_name))

class Flight(models.Model):
    # flight number (e.g. BA1349)
    flight_num = models.CharField(max_length=10, default="unspecified")
    # departue airport (e.g. London Heathrow LHR)
    dep_airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name="dep_airport")
    # destination airport (e.g. New York JFK)
    dest_airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name="dest_airport")
    # departure date-time (e.g. 2018.04.01, 14:45:00)
    dep_datetime = models.DateTimeField(default=timezone.now)
    # arrival date-time (e.g. 2018.04.01, 20:30:00)
    arr_datetime = models.DateTimeField(default=timezone.now)
    #  flight duration (e.g. 5:15:00, i.e. 5 hours and 15 minutes)
    duration = models.DurationField(default=0)
    # aircraft type used for this flight (a foreign key to aircraft table)
    aircraft_type = models.ForeignKey('Aircraft', null="True", on_delete=models.CASCADE)
    # price of a single seat on this Flight
    price = models.FloatField(default=0)

    def __str__(self):
        return ("%s" % (self.flight_num))

class Booking(models.Model):
    # unique booking number (e.g. WXY12Z)
    booking_number = models.CharField(max_length=10, unique=True)
    # flight associated with this booking (a foreign key to the flights table)
    booking_flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    # number of seats booked.
    booked_seats = models.IntegerField(default="unspecified")
    # passengers
    #passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE)
    # status of this booking (ONHOLD, CONFIRMED, CANCELLED, or TRAVELLED)
    #STATUS_CHOICES = (('ONHOLD', 'ONHOLD'), ('CONFIRMED','CONFIRMED'), ('CANCELLED', 'CANCELLED'), ('TRAVELLED','TRAVELLED'))
    booking_status = models.CharField(max_length=10, default='ON_HOLD')
    #  time this booking will no longer be valid if the status of the booking is ONHOLD.
    time_to_complete = models.IntegerField(null=True)

    def __str__(self):
        return ("%s" % (self.booking_number))


class Passenger(models.Model):
    # details of each passenger  (first name, surname, email, and phone number).
    booking_number = models.ForeignKey('Booking', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default="unspecified")
    surname = models.CharField(max_length=50, default="unspecified")
    email = models.EmailField(max_length=50, default="unspecified@unspecified.com")
    phone = models.CharField(max_length=15, default="unspecified")

    def __str__(self):
        return ("%s %s" % (self.first_name, self.surname))

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

    def __str__(self):
        return ("%s" % (self.name))


class Invoice(models.Model):
    #  unique reference number for this invoice at the airline’s database
    # reference_number = models.IntegerField(primary_key=True, editable=False) #--- substituted by the id
    # reference_number = models.CharField(max_length=20, default="unknown") #--- substituted by the id

    # unique reference number for this invoice within the database of the payment service provider
    #  booking number for which the invoice was issued.
    booking_number = models.ForeignKey('Booking', on_delete=models.CASCADE)
    #  amount of the invoice
    amount = models.FloatField(default="unspecified")
    # paid or not
    paid = models.BooleanField(default=False)
    # electronic stamp (10 autogenerated digit alphanumeric )
    stamp = models.CharField(max_length=10, default="")

    def __str__(self):
        return ("Invoice for %s" % (self.booking_number))
