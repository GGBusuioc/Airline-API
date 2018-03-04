from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import *
from django.core import serializers
from bson import json_util
from datetime import datetime


# Create your views here.



def findflight(request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    departue_airport = body['departue_airport']
    destination_airport = body['destination_airport']
    date = body['date']
    is_flexible = body['is_flexible']

    datetime_object = datetime.strptime(date, '%m-%d-%Y')
    #d_truncated = datetime.date(datetime_object.year, datetime_object.month, datetime_object.day)
    print(datetime_object)


    print(datetime_object.day)
    if is_flexible == 'Y':
        all_entries = Flight.objects.filter(departue_airport=departue_airport,
                                            destination_airport=destination_airport,
                                            end__year=datetime_object.year, end__month=datetime_object.month, end__day=datetime_object.day,
                                            )
    
    else:
        all_entries = Flight.objects.filter(departue_airport=departue_airport, destination_airport=destination_airport)


    flight_results = []

    for entry in all_entries:
        flight_result = []
        flight_result.append(entry.flight_number)
        flight_result.append(entry.departue_airport)
        flight_result.append(entry.destination_airport)
        flight_result.append(entry.departue_datetime)
        flight_results.append(flight_result)

    # How to serialize a queryset object
    #data = serializers.serialize('json', list(all_entries), fields=('flight_number'))
    if flight_results:
        return JsonResponse(json.dumps(flight_results, default=json_util.default), safe=False)
    else:
        return HttpResponse("Seems like nothing was found",status=503)
