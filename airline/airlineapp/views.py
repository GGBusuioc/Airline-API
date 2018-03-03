from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import requests
# Create your views here.



def findflight(request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    departue_airport = body['departue_airport']
    destination_airport = body['destination_airport']
    date = body['date']



    payload = {
        'departue_airport' : departue_airport,
        'destination_airport': destination_airport,
        'date': date,
    }

    return JsonResponse(payload)
