import requests
import json
from bson import json_util
import datetime

print("Welcome to the client!")

process_complete = False

while process_complete == False:

    print("1. Find a flight")
    action = 'findflight'
    print("Pick a DEPARTUE AIRPORT,  DESTINATION AIPORT, DATE (YYYY-MM-DD), NUMBER OF PASSENGERS, FLEXIBLE (Y or N only)")
    #user_input = input()
    try:
        #dep_airport, dest_airport, dep_date, int(num_passengers), is_flex = user_input.split(" ")
        dep_airport = "Leeds"
        dest_airport = "Luton"
        dep_date = "2018-03-01"
        num_passengers = 2
        is_flex = "Y"


    except ValueError:
        print("Please provide all the required parameters")


    url = 'http://localhost:8000/findflight/'
    payload = {
        'dep_airport' : dep_airport,
        'dest_airport': dest_airport,
        'dep_date': dep_date,
        'num_passengers': num_passengers,
        'is_flex': is_flex,
    }

    r = requests.get(url, data=json.dumps(payload))
    print(r.json())
    try:
        flights = json.loads(r.json())
        #print(flights)
        print("*************************************")
        print("FLIGHT ID | FLIGHT NR | DEP AIR | DEST AIR | DEP D&T | ARI D&T | DURATION [H, M] | PRICE £")
        print("\n")


        for result in flights["flights"]:
            print(str(result['flight_id']) + " " + result['flight_num'] + " " + result['dep_airport'] + " " + result['dest_airport']+ " " + str(result['dep_datetime']) + " " + str(result['arr_datetime']) + " " + str(result['duration']) + " " + str(result['price']))
        print("*************************************")

    except ValueError:
        print("Nothing was found. A reason plus the payload. ")

    print("\n2. Book a flight\n")

    print("Pick a FLIGHT ID, FIRSTNAME, SURNAME, EMAIL, PHONE")

    payload_list = []

    while num_passengers > 0:
        print("PLEASE INTRODUCE THE INFORMATION FOR THE %d PASSENGER" % (num_passengers))
        user_input = input()
        num_passengers = num_passengers - 1
        try:
            flight_id, first_name, surname, email, phone = user_input.split(" ")
        except ValueError:
            print("Please provide all the required parameters")

        print("These are the params provided: %s %s %s %s %s" % (flight_id, first_name,  surname, email, phone))

        url = 'http://localhost:8000/bookflight/'
        payload_elem = {
            'flight_id': flight_id,
            'first_name': first_name,
            'surname': surname,
            'email': email,
            'phone': phone,
        }

        payload_list.append(payload_elem)
    print("Sending the request")
    print(payload_list)
    r = requests.post(url, data=json.dumps(payload_list))

    print("This is what I have received from the server\n")
    print(r.json())
