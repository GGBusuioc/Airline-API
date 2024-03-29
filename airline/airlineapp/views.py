from django.shortcuts import render
from django.http import HttpResponse, Http404
import json
from bson import json_util
from .models import *
from django.core import serializers
import datetime
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
import random
import string
from django.db.models import Sum
import requests


def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def stamp_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def findflight(request, format=None):
    if request.method =="GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        # test if the departue airport appears in the database
        try:
            dep_airport = Airport.objects.get(airport_name=body['dep_airport'])
        except:
            return HttpResponse("Sorry. The DEPARTUE AIPORT %s is not stored in our airports database" % (body['dep_airport']), content_type="text/plain", status=503)
        # test if the destination airport appears in the database
        try:
            dest_airport = Airport.objects.get(airport_name=body['dest_airport'])
        except:
            return HttpResponse("Sorry. The DESTINATION AIRPORT %s is not stored in our airports database" % (body['dest_airport']), content_type="text/plain", status=503)


        dep_date = body['dep_date']
        num_passengers = body['num_passengers']
        is_flex = body['is_flex']

        try:
            datetime_object = datetime.datetime.strptime(dep_date, '%Y-%m-%d')
        except:
            return HttpResponse("Sorry. %s does no comply to our format standards." % (body['dep_date']), content_type="text/plain", status=503)


        try:
            if is_flex == True or is_flex == 'y' or is_flex == 'Y' or is_flex == 'yes' or is_flex == 'Yes':
                all_entries = Flight.objects.filter(dep_airport=dep_airport,
                                                    dest_airport=dest_airport,
                                                    dep_datetime__range=[datetime_object + datetime.timedelta(days=-3), datetime_object + datetime.timedelta(days=3)]
                                                    )
            elif is_flex == False or is_flex == 'n' or is_flex == 'N' or is_flex == 'no' or is_flex == 'No':
                    all_entries = Flight.objects.filter(dep_airport=dep_airport,
                                                        dest_airport=dest_airport,
                                                        dep_datetime__day=datetime_object.day,
                                                        dep_datetime__month=datetime_object.month,
                                                        dep_datetime__year=datetime_object.year,
                                                        )
            else:
                all_entries = []
                return HttpResponse("Sorry. %s is not one of the two possible options for FLEXIBILITY. Try y/n." % (body['is_flex']), content_type="text/plain", status=503)

        except:
            return

        flight_results = []

        for entry in all_entries:
            flight_result = {}

            flight_result['flight_id'] = str(entry.pk)
            flight_result['flight_num'] = entry.flight_num
            flight_result['dep_airport'] = str(dep_airport)
            flight_result['dest_airport'] = str(dest_airport)
            flight_result['dep_datetime'] = str(entry.dep_datetime)
            flight_result['arr_datetime'] = str(entry.arr_datetime)
            flight_result['duration'] = str(entry.duration)
            flight_result['price'] = str(entry.price)

            flight_results.append(flight_result)


        findflight = {}
        findflight['flights'] = flight_results

        if all_entries:
            return HttpResponse(json.dumps(findflight), content_type="application/json")
        else:
            return HttpResponse("Service Unavailable",  content_type="text/plain", status=503)

@csrf_exempt
def bookflight(request):
    if request.method=="POST" or "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        final_list = []

        booking_num = random_generator()

        flight_object = Flight.objects.get(id=body['flight_id'])

        aircraft_type = flight_object.aircraft_type
        aircraft_object = Aircraft.objects.get(aircraft_type=aircraft_type)
        num_of_passengers_allowed = aircraft_object.aircraft_number_seats
        thesum = Booking.objects.filter(booking_flight=flight_object).aggregate(Sum('booked_seats'))

        # find the bookings already made

        # should check if a booking can be made
        if(thesum['booked_seats__sum'] is None):
            seats_booked = 0
        else:
            seats_booked = thesum['booked_seats__sum']

        if(seats_booked+len(body['passengers']) <= num_of_passengers_allowed):

            Booking.objects.create(booking_number = booking_num,
                                    booking_flight = flight_object,
                                    booked_seats = len(body['passengers']),
                                    booking_status = "ON_HOLD",
                                    time_to_complete = 30,
            )

            booking_object = Booking.objects.get(booking_number=booking_num)
            for result in body['passengers']:
                first_name = result['first_name']
                surname = result['surname']
                email = result['email']
                phone = result['phone']
                Passenger.objects.create(booking_number=booking_object,first_name=first_name,surname =surname,email = email,phone = phone)


            payload = {}
            payload['booking_num'] = booking_num
            payload['booking_status'] = "ON_HOLD"
            payload['tot_price'] = booking_object.booked_seats * flight_object.price
            global tot_price
            tot_price = booking_object.booked_seats * flight_object.price
        else:
            return HttpResponse("WE ARE FULL BOOKED SORRY!", content_type="text/plain")


        if payload:
            return HttpResponse(json.dumps(payload), content_type="application/json", status=201)
        else:
            return HttpResponse("Something went wrong ", content_type="text/plain")

def paymentmethods(request):
    if request.method == "GET":
        providers_list = []

        payment_objects = PaymentProvider.objects.all()

        for entry in payment_objects:
            payment_result = {}
            payment_result['pay_provider_id'] = entry.id
            payment_result['pay_provider_name'] = entry.name
            providers_list.append(payment_result)

        payload = {}
        payload['pay_providers'] = providers_list
        if payload:
            return HttpResponse(json.dumps(payload), content_type="application/json")
        else:
            return HttpResponse("Service Unavailable", content_type="text/plain" ,status=503)

@csrf_exempt
def payforbooking(request):
    if request.method == "POST":

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        payment_object = PaymentProvider.objects.get(id=body["pay_provider_id"])

        session = requests.session()

        b = session.post(payment_object.website+"api/login/",headers={'content-type':"application/x-www-form-urlencoded"}, data = {'username':payment_object.login_name,'password':payment_object.password})

        try:
            booking_object = Booking.objects.get(booking_number=body["booking_num"])

        except:
            return HttpResponse("Sorry. The BOOKING NUMBER %s is not not storred in our database." % (body['booking_num']), content_type="text/plain", status=503)

        payload = {}
        payload['account_num'] = payment_object.account_number
        payload['client_ref_num'] = booking_object.booking_number
        payload['amount'] = booking_object.booked_seats*booking_object.booking_flight.price

        r = session.post(payment_object.website+"api/createinvoice/", headers={'content-type':"application/json"}, data = json.dumps(payload))

        createinvoice_payload = json.loads(r.text)

        try:
            invoice = Invoice(booking_number = booking_object, amount = booking_object.booked_seats*booking_object.booking_flight.price, stamp = createinvoice_payload['stamp_code'])
            invoice.save()
        except:
            print("Invoice not created")


        try:
            invoice = Invoice.objects.get(booking_number=booking_object)
        except:
            return HttpResponse("Sorry. There is no INVOICE ID for %s" % (body['booking_num']),  content_type="text/plain", status=503)

        payload = {}
        payload['payprovider_ref_num'] = createinvoice_payload['payprovider_ref_num']
        payload['client_ref_num'] = booking_object.booking_number
        payload['amount'] = booking_object.booked_seats*booking_object.booking_flight.price

        r = session.post(payment_object.website+"api/payinvoice/", headers={'content-type':"application/json"}, data = json.dumps(payload))


        payload = {}
        payload["pay_provider_id"] = body["pay_provider_id"]
        payload["invoice_id"] = invoice.id
        payload["booking_num"] = body["booking_num"]
        payload["url"] = payment_object.website
        payload["payprovider_ref_num"] =  createinvoice_payload['payprovider_ref_num']
        #


        if payload:
            return HttpResponse(json.dumps(payload), content_type="application/json", status=201)
        else:
            return HttpResponse("Service Unavailable",  content_type="text/plain", status=503)


@csrf_exempt
def finalizebooking(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        booking_object = Booking.objects.get(booking_number=body["booking_num"])
        booking_object.booking_status = "CONFIRMED"
        booking_object.save()
        payload = {}
        payload["booking_num"] = booking_object.booking_number
        payload["booking_status"] = booking_object.booking_status

        return HttpResponse(json.dumps(payload), content_type="application/json", status=201)

def bookingstatus(request):
    if request.method=="GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        try:
            booking_object = Booking.objects.get(booking_number=body["booking_num"])
        except:
            return HttpResponse("Sorry. There is no BOOKING for the following BOOKING NUMBER: %s" % (body['booking_num']), status=503)

        flight_object = Flight.objects.get(flight_num=booking_object.booking_flight)

        payload = {}
        payload["booking_num"] = body["booking_num"]
        payload["booking_status"] = booking_object.booking_status
        payload["flight_num"] = flight_object.flight_num
        payload["dep_airport"] = str(flight_object.dep_airport)
        payload["dest_airport"] = str(flight_object.dest_airport)
        payload["dep_datetime"] = str(flight_object.dep_datetime)
        payload["arr_datetime"] = str(flight_object.arr_datetime)
        payload["duration"] = str(flight_object.duration)
        if payload:
            return HttpResponse(json.dumps(payload), content_type="application/json", status=200)
        else:
            return HttpResponse("Service Unavailable", status=503)


@csrf_exempt
def cancelbooking(request):
    if request.method=="POST":

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        try:
            booking_object = Booking.objects.get(booking_number=body["booking_num"])
        except:
            return HttpResponse("Sorry. There is no BOOKING for the following BOOKING NUMBER: %s" % (body['booking_num']), status=503)

        booking_object.booking_status = "CANCELLED"
        booking_object.save()

        payload = {}
        payload["booking_num"] = body["booking_num"]
        payload["booking_status"] = "CANCELLED"

        if payload:
            return HttpResponse(json.dumps(payload), content_type="application/json", status=201)
        else:
            return HttpResponse("Service Unavailable", status=503)
