import requests
import json
from bson import json_util
import datetime

print("Welcome to the client!")

process_complete = False

while process_complete == False:

    print("1. Find a flight")
    print("Pick a DEPARTUE AIRPORT,  DESTINATION AIPORT, DATE (YYYY-MM-DD), NUMBER OF PASSENGERS, FLEXIBLE (Y or N only)")
    user_input = input()
    try:
        dep_airport, dest_airport, dep_date, num_passengers, is_flex = user_input.split(" ")

        # dep_airport = "Leeds"
        # dest_airport = "Luton"
        # dep_date = "2018-03-01"
        # num_passengers = 2
        # is_flex = "Y"


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
        print(r.text)

    # print("\n2. Book a flight\n")
    #
    # print("Pick a FLIGHT ID, FIRSTNAME, SURNAME, EMAIL, PHONE")
    #
    # payload_list = []
    #
    # print("PLEASE INTRODUCE THE FLIGHT_ID")
    # flight_id = input()
    #
    # while num_passengers > 0:
    #     print("PLEASE INTRODUCE THE INFORMATION FOR THE %d PASSENGER" % (num_passengers))
    #     num_passengers = num_passengers - 1
    #     user_input = input()
    #     try:
    #         first_name, surname, email, phone = user_input.split(" ")
    #         print(first_name)
    #     except ValueError:
    #         print("Please provide all the required parameters")
    #
    #     print("These are the params provided: %s %s %s %s" % (first_name,  surname, email, phone))
    #
    #     url = 'http://localhost:8000/bookflight/'
    #
    #     payload_elem = {
    #         'first_name': first_name,
    #         'surname': surname,
    #         'email': email,
    #         'phone': phone,
    #     }
    #
    #
    #
    #     payload_list.append(payload_elem)
    #
    #     passengers = {}
    #     passengers['flight_id'] = flight_id
    #     passengers['passengers'] = payload_list
    # #
    # print("Sending the PASSENGERS request")
    # print(json.dumps(passengers))
    # r = requests.post(url, data=json.dumps(passengers))
    #
    #

    print("3. Request PAYMENT METHODS")

    url = 'http://localhost:8000/paymentmethods/'

    b = requests.get(url)
    pay_providers = json.loads(b.text)
    print("PAYMENT PROVIDER ID | PAYMENT PROVIDER NAME")

    for result in pay_providers["pay_providers"]:
        print(str(result['pay_provider_id']) + " " + result['pay_provider_name'])



    process_complete = True
