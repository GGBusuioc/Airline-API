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

        dep_airport = Airport.objects.get(airport_name=body['dep_airport'])
        dest_airport = Airport.objects.get(airport_name=body['dest_airport'])

        dep_date = body['dep_date']
        num_passengers = body['num_passengers']
        is_flex = body['is_flex']


        datetime_object = datetime.datetime.strptime(dep_date, '%Y-%m-%d')
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

        # How to serialize a queryset object
        #data = serializers.serialize('json', list(all_entries), fields=('flight_number'))

        if findflight:
            return JsonResponse(json.dumps(findflight), safe=False)
        else:
            return HttpResponse("Seems like nothing was found", status=503)

@csrf_exempt
def bookflight(request):
    if request.method=="POST":
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
            print("payload before sending")
            print(json.dumps(payload))
        else:
            return HttpResponse("WE ARE FULL BOOKED SORRY!")

        if payload:
            return HttpResponse("YOU ARE LUCKY. WE ARE NOT FULL BOOKED YET",json.dumps(payload), status=204)
        else:
            return Http404("So  mething went wrong ")

def paymentmethods(request):

    providers_list = []

    payment_objects = PaymentProvider.objects.all()

    for entry in payment_objects:
        payment_result = {}
        payment_result['pay_provider_id'] = entry.id
        payment_result['pay_provider_name'] = entry.name
        providers_list.append(payment_result)



    payload = {}
    payload['pay_providers'] = providers_list


    return HttpResponse(json.dumps(payload))
