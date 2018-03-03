from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import *
from django.core import serializers

# Create your views here.



def findflight(request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    departue_airport = body['departue_airport']
    destination_airport = body['destination_airport']

    all_entries = Flight.objects.filter(departue_airport=departue_airport, destination_airport=destination_airport)

    flight_numbers = []
    for entry in all_entries:
        flight_numbers.append(entry.flight_number)

    # How to serialize a queryset object
    #data = serializers.serialize('json', list(all_entries), fields=('flight_number'))

    return JsonResponse(json.dumps(flight_numbers), safe=False)
