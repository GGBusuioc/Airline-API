from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
import json
from .models import *
from django.core import serializers
from bson import json_util
import datetime
from datetime import timedelta


# Create your views here.

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds

def findflight(request, format=None):
    if request.method =="GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        #dep_airport = body['dep_airport']
        print(body['dep_airport'])
        dep_airport = Airport.objects.get(airport_name=body['dep_airport'])
        #dest_airport = body['dest_airport']
        dest_airport = Airport.objects.get(airport_name=body['dest_airport'])
        print(type(dest_airport))
        # print(type(str(dest_airport)))
        # string_dep_airport =
        # string_dest_airport =

        dep_date = body['dep_date']
        num_passengers = body['num_passengers']
        is_flex = body['is_flex']


        datetime_object = datetime.datetime.strptime(dep_date, '%Y-%m-%d')
        #d_truncated = datetime.date(datetime_object.year, datetime_object.month, datetime_object.day)

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
            flight_result = []
            # converting the duration to hours and minutes
            hours, minutes, seconds = convert_timedelta(entry.duration)
            duration = (hours, minutes)

            flight_result.append(entry.id)
            flight_result.append(entry.flight_num)
            flight_result.append(str(dep_airport))
            flight_result.append(str(dest_airport))
            flight_result.append(entry.dep_datetime)
            flight_result.append(entry.arr_datetime)
            flight_result.append(duration)
            flight_result.append(entry.price)
            flight_results.append(flight_result)

        # How to serialize a queryset object
        #data = serializers.serialize('json', list(all_entries), fields=('flight_number'))

        if flight_results:
            return JsonResponse(json.dumps(flight_results, default=json_util.default), safe=False)
        else:
            return HttpResponse("Seems like nothing was found", status=503)
