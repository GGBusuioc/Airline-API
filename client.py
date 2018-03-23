import requests
import json
from bson import json_util
import datetime

print("Welcome to the client!")

process_complete = False

while process_complete == False:



########################### PART 1 ################################
    print("1. Find a flight")
    print("Pick a DEPARTUE AIRPORT,  DESTINATION AIPORT, DATE (YYYY-MM-DD), NUMBER OF PASSENGERS, FLEXIBLE (Y or N only)")
    #user_input = input()
    # try:
        #dep_airport, dest_airport, dep_date, num_passengers, is_flex = user_input.split(" ")

    dep_airport = "Leeds"
    dest_airport = "Luton"
    dep_date = "2018-03-01"
    num_passengers = 1
    is_flex = "N"


    # except ValueError:
    #     print("Please provide all the required parameters")


    url = 'http://localhost:8000/api/findflight/'
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

########################### PART 2 ################################
    print("\n2. Book a flight\n")

    print("Pick a FLIGHT ID, FIRSTNAME, SURNAME, EMAIL, PHONE")

    payload_list = []

    print("PLEASE INTRODUCE THE FLIGHT_ID")
    flight_id = input()

    while num_passengers > 0:
        print("PLEASE INTRODUCE THE INFORMATION FOR THE %d PASSENGER" % (num_passengers))
        num_passengers = num_passengers - 1
        user_input = input()
        try:
            first_name, surname, email, phone = user_input.split(" ")
            print(first_name)
        except ValueError:
            print("Please provide all the required parameters")

        print("These are the params provided: %s %s %s %s" % (first_name,  surname, email, phone))

        url = 'http://localhost:8000/api/bookflight/'

        payload_elem = {
            'first_name': first_name,
            'surname': surname,
            'email': email,
            'phone': phone,
        }



        payload_list.append(payload_elem)

        passengers = {}
        passengers['flight_id'] = flight_id
        passengers['passengers'] = payload_list
    #

    r = requests.post(url, data=json.dumps(passengers))
    # try statement needed
    response_r = json.loads(r.text)
    print("BOOKING NUMBER | BOOKING STATUS | TOTAL PRICE")
    print(response_r["booking_num"] + " " +response_r["booking_status"] + " " +str(response_r["tot_price"]))

########################### PART 3 ################################

    print("3. Request PAYMENT METHODS")

    url = 'http://localhost:8000/api/paymentmethods/'

    b = requests.get(url)
    pay_providers = json.loads(b.text)
    print("PAYMENT PROVIDER ID | PAYMENT PROVIDER NAME")

    for result in pay_providers["pay_providers"]:
        print(str(result['pay_provider_id']) + " " + result['pay_provider_name'])



########################### PART 4 ################################

    print("4. PAY FOR BOOKING")
    print("Please insert your BOOKING NUMBER and your PAYMENT PROVIDER ID | USERNAME | PASSWORD")
    user_input = input()
    try:
        booking_num, pay_provider_id = user_input.split(" ")
    except ValueError:
        print("Please provide all the required parameters")

    booking_payload = {}
    booking_payload['booking_num'] = booking_num
    booking_payload['pay_provider_id'] = pay_provider_id




    url = 'http://localhost:8000/api/payforbooking/'
    b = requests.post(url, data=json.dumps(booking_payload))

    try:
        response = json.loads(b.text)
        print(" INVOICE ID | URL | PAY PROVIDER ID | BOOKING NUM")

        print(str(response["invoice_id"]) + " " + str(response["pay_provider_id"]) + " " + response["url"] + " " + response["booking_num"] )
    except ValueError:
        print(b.text)

    # loging with personal account
    print("PLEASE ENTER YOUR PERSONAL USERNAME AND PASSWORD TO PAY FOR THE INVOICE")
    user_input = input()
    try:
        username, password = user_input.split(" ")
    except ValueError:
        print("Please provide all the required parameters")



    # payload['payprovider_ref_num'] = createinvoice_payload['payprovider_ref_num']
    # payload['client_ref_num'] = booking_object.booking_number
    # payload['amount'] = booking_object.booked_seats*booking_object.booking_flight.price
    # print(json.dumps(payload))


    session = requests.session()
    b = session.post(response["url"]+"api/login/", data = {'username':username,'password':password})
    print(b.status_code)
    payload = {}
    payload['payprovider_ref_num'] = response['payprovider_ref_num']
    payload['client_ref_num'] = response["booking_num"]
    payload['amount'] = response_r["tot_price"]

    r = session.post(response["url"]+"api/payinvoice/", headers={'content-type':"application/json"}, data = json.dumps(payload))
    print(r.status_code)
    print(r.text)

########################### PART 5 ################################

    print("5. Finalize Booking")
    print("Please insert your BOOKING NUMBER, PAYMENT PROVIDER IDENTIFIER, PAYMENT PROVIDER ELECTRONIC STAMP")
    user_input = input()
    try:
        booking_num, pay_provider_id, stamp = user_input.split(" ")
    except ValueError:
        print("Please provide all the required parameters")

    finalize_booking_payload = {}
    finalize_booking_payload['booking_num'] = booking_num
    finalize_booking_payload['pay_provider_id'] = pay_provider_id
    finalize_booking_payload['stamp'] = stamp

    url = 'http://localhost:8000/api/finalizebooking/'
    b = requests.post(url, data=json.dumps(finalize_booking_payload))

    try:
        response = json.loads(b.text)
        print(response)
    except ValueError:
        print(b.text)





########################### PART 6 ################################

    # print("BOOKING STATUS Part 6")
    # print("Please insert your BOOKING NUMBER")
    # user_input = input()
    # try:
    #     booking_num = user_input
    # except:
    #     print("Please provide all the required parameters")
    # status_payload = {}
    # status_payload["booking_num"] = booking_num
    # url = 'http://localhost:8000/api/bookingstatus/'
    # r = requests.get(url, data=json.dumps(status_payload))
    #
    # try:
    #     response = json.loads(r.text)
    #     print("BOOKING NUM | BOOKING STATUS | FLIGHT NUM | DEP AIRPORT | DEST AIRPORT | DEP DATETIME | ARR DATETIME | DURATION")
    #     print(response["booking_num"] + " " +response["booking_status"] + " " +response["flight_num"] + " " +response["dep_airport"] + " " +response["dest_airport"] + " " +response["dep_datetime"] + " " +response["arr_datetime"] + " " +response["duration"] )
    # except ValueError:
    #     print(r.text)

########################### PART 7 ################################

    print("CANCEL BOOKING Part 7")
    print("Please insert your BOOKING NUMBER")
    user_input = input()
    try:
        booking_num = user_input
    except:
        print("Please provide all the required parameters")
    cancel_payload = {}
    cancel_payload["booking_num"] = booking_num
    url = 'http://localhost:8000/api/cancelbooking/'
    r = requests.post(url, data=json.dumps(cancel_payload))

    try:
        response = json.loads(r.text)
        print("BOOKING NUMBER | BOOKING STATUS")
        print(response["booking_num"] + " " + response["booking_status"])
    except ValueError:
        print(r.text)


    process_complete = True
