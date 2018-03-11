from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
import json
from .models import *
from django.core import serializers
from bson import json_util
import datetime
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
import random
import string
from django.db.models import Sum

def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def findflight(request, format=None):
    if request.method =="GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        # test if the departue airport appears in the database
        try:
            dep_airport = Airport.objects.get(airport_name=body['dep_airport'])
        except:
            return HttpResponse("Sorry. The DEPARTUE AIPORT %s is not stored in our airports database" % (body['dep_airport']), status=503)
        # test if the destination airport appears in the database
        try:
            dest_airport = Airport.objects.get(airport_name=body['dest_airport'])
        except:
            return HttpResponse("Sorry. The DESTINATION AIRPORT %s is not stored in our airports database" % (body['dest_airport']), status=503)


        #return HttpResponse("One of the airports is not found", status=503)

        dep_date = body['dep_date']
        num_passengers = body['num_passengers']
        is_flex = body['is_flex']

        try:
            datetime_object = datetime.datetime.strptime(dep_date, '%Y-%m-%d')
        except:
            return HttpResponse("Sorry. %s does no comply to our format standards." % (body['dep_date']), status=503)


        try:
            if is_flex == 'Y':
                all_entries = Flight.objects.filter(dep_airport=dep_airport,
                                                    dest_airport=dest_airport,
                                                    dep_datetime__range=[datetime_object + datetime.timedelta(days=-3), datetime_object + datetime.timedelta(days=3)]
                                                    )
            elif is_flex == 'N':
                    all_entries = Flight.objects.filter(dep_airport=dep_airport,
                                                        dest_airport=dest_airport,
                                                        dep_datetime__day=datetime_object.day,
                                                        )
            else:
                all_entries = []
                return HttpResponse("Sorry. %s is not one of the two possible options for FLEXIBILITY" % (body['is_flex']), status=503)

        except:
            return

        flight_results = []

        for entry in all_entries:
            flight_result = {}

            flight_result['flight_id'] = entry.pk
            flight_result['flight_num'] = entry.flight_num
            flight_result['dep_airport'] = str(dep_airport)
            flight_result['dest_airport'] = str(dest_airport)
            flight_result['dep_datetime'] = str(entry.dep_datetime)
            flight_result['arr_datetime'] = str(entry.arr_datetime)
            flight_result['duration'] = str(entry.duration)
            flight_result['price'] = entry.price

            flight_results.append(flight_result)

        findflight = {}
        findflight['flights'] = flight_results


        if findflight:
            return JsonResponse(json.dumps(findflight), safe=False)
        else:
            return HttpResponse("Service Unavailable", status=503)

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

        else:
            return HttpResponse("WE ARE FULL BOOKED SORRY!")


        if payload:
            return HttpResponse(json.dumps(payload), status=201)
        else:
            return Http404("So  mething went wrong ")

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
            return HttpResponse(json.dumps(payload))
        else:
            return HttpResponse("Service Unavailable", status=503)

@csrf_exempt
def payforbooking(request):
    if request.method == "POST":

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        print(body)
        payment_object = PaymentProvider.objects.get(id=body["pay_provider_id"])
        print(payment_object)
        payload = {}
        payload["pay_provider_id"] = body["pay_provider_id"]
        payload["invoice_id"] = 0
        payload["booking_num"] = body["booking_num"]

        payload["url"] = payment_object.website


        if payload:
            return HttpResponse(json.dumps(payload), status=201)
        else:
            return HttpResponse("Service Unavailable", status=503)

def finalizebooking(request):
    return ("WORK IN PROGRESS")

def bookingstatus(request):
    return ("WORK IN PROGRESS")

def cancelbooking(request):
    return ("WORK IN PROGRESS")
