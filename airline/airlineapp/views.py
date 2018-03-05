from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import *
from django.core import serializers
from bson import json_util
import datetime
from datetime import timedelta


# Create your views here.



def findflight(request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    departue_airport = body['departue_airport']
    destination_airport = body['destination_airport']
    date = body['date']
    number_of_tickets = body['number_of_tickets']
    is_flexible = body['is_flexible']

    datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d')
    #d_truncated = datetime.date(datetime_object.year, datetime_object.month, datetime_object.day)


    if is_flexible == 'Y':
        all_entries = Flight.objects.filter(departue_airport=departue_airport,
                                            destination_airport=destination_airport,
                                            departue_datetime__range=[datetime_object + datetime.timedelta(days=-3), datetime_object + datetime.timedelta(days=3)]
                                            )

    elif is_flexible == 'N':
            all_entries = Flight.objects.filter(departue_airport=departue_airport,
                                                destination_airport=destination_airport,
                                                departue_datetime__day=datetime_object.day,
                                                )

    flight_results = []

    for entry in all_entries:
        flight_result = []
        flight_result.append(entry.flight_number)
        flight_result.append(entry.departue_airport)
        flight_result.append(entry.destination_airport)
        flight_result.append(entry.departue_datetime)
        flight_result.append(entry.arrival_datetime)
        flight_result.append(datetime.datetime.strptime(str(entry.duration), '%H:%M:%S'))
        flight_result.append(entry.ticket_price)
        flight_results.append(flight_result)

    # How to serialize a queryset object
    #data = serializers.serialize('json', list(all_entries), fields=('flight_number'))
    if flight_results:
        return JsonResponse(json.dumps(flight_results, default=json_util.default), safe=False)
    else:
        return HttpResponse("Seems like nothing was found",status=503)
