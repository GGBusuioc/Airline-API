import requests
import json

print("Welcome to the client!")

process_complete = False

while process_complete == False:

    print("=====================================")
    print("1. Find a flight")
    action = 'findflight'
    print("Pick a DEPARTUE AIRPORT,  DESTINATION AIPORT and DATE")
    user_input = input()
    # /findflight/departue_airport/destination_airport/date/
    try:
        departue, destination, date = user_input.split(" ")
    except ValueError:
        print("Please provide all the required parameters")


    #print("This is your json object: " + json_str)
    url = 'http://localhost:8000/findflight/'
    payload = {
        'departue_airport' : departue,
        'destination_airport': destination,
        'date': date,
    }
    #headers = {'content-type': 'application/json; charset=utf-8'}

    r = requests.get(url, data=json.dumps(payload))
    print(r.json())
