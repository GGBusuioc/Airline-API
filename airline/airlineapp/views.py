from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
import json
from .models import *
from django.core import serializers
from bson import json_util
import datetime
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from copy import deepcopy

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

        #print(body[0])
        final_list = []
        for result in body:
            first_name = result['first_name']
            surname = result['surname']
            email = result['email']
            phone = result['phone']
            Passenger.objects.create(first_name=first_name,surname =surname,email = email,phone = phone)
            passenger_entry = Passenger.objects.get(first_name=first_name,surname = surname,email = email,phone = phone)

            this_result = {}
            this_result['first_name'] = passenger_entry.first_name
            this_result['surname'] = passenger_entry.surname
            this_result['email'] = passenger_entry.email
            this_result['phone'] = passenger_entry.phone

            final_list.append(this_result)
            #print("This is the final list")
            print(final_list)



        if final_list:
            return JsonResponse(json.dumps(final_list), safe=False)
        else:
            return HttpResponse("Something went wrong in the booking process", status=503)
