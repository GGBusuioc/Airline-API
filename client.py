import requests
import json
from bson import json_util
import datetime


process_complete = False


print("******************************************************************************************")
print("******************************************************************************************")
print("***                                                                                   ****")
print("**                  Welcome to COMP3011 - Web Servicies and Web Data                    **")
print("*                                                                                        *")
print("*                                                                                        *")
print("*                               Coursework 1                                             *")
print("*                             Client application                                         *")
print("*                                                                                        *")
print("*                       API implemented: Airline API                                     *")
print("*                               made by: George-Gabriel Busuioc                          *")
print("**                                                                                      **")
print("***                                                                                    ***")
print("******************************************************************************************")
print("******************************************************************************************")


while process_complete == False:



########################### PART 1 ################################

    print("                 1. FIND FLIGHTS                  ")

    # print("Pick a DEPARTUE AIRPORT,  DESTINATION AIPORT, DATE (YYYY-MM-DD), NUMBER OF PASSENGERS, FLEXIBLE (True or False only)")
    # #user_input = input()
    # # try:
    #     #dep_airport, dest_airport, dep_date, num_passengers, is_flex = user_input.split(" ")
    #

    dep_airport = "LBA"
    dest_airport = "MAN"
    dep_date = "2018-03-17"
    num_passengers = 1
    is_flex = 'y'


    #
    # dep_airport = "FCO"
    # dest_airport = "BER"
    # dep_date = "2018-05-05"
    # num_passengers = 1
    # is_flex = 'y'
    #



###################################################################
###################### FIND FLIGHT ################################
###################################################################
    chosen_url = 'http://localhost:8000'


# get all the airlines from the directory
    url = 'http://directory.pythonanywhere.com/api/list/'


    # payload = {
    #     'company_type': "payment",
    # }

    payload = {
        'company_type': "airline",
    }

    #r = requests.get(url, headers={'content-type':'application/json'}, data=json.dumps(payload))

    # FOR AGGREGAT


    payload = {
        'dep_airport' : dep_airport,
        'dest_airport': dest_airport,
        'dep_date': dep_date,
        'num_passengers': num_passengers,
        'is_flex': is_flex,
    }



    # r = requests.get(url, headers={'content-type':'application/json'}, data=json.dumps(payload))
    #r = requests.get('http://ggbusuioc.pythonanywhere.com/api/findflight/', data=json.dumps(payload))
    r = requests.get('http://localhost:8000/api/findflight/', headers={'Content-Type': 'application/json'}, data=json.dumps(payload))


    # print(r.headers['Content-Type'])
    # print(r.text)

    # payload = {
    #     'dep_airport' : dep_airport,
    #     'dest_airport': dest_airport,
    #     'dep_date': dep_date,
    #     'num_passengers': num_passengers,
    #     'is_flex': is_flex,
    # }
    #
    airlines = json.loads(r.text)
    print(airlines)
    for result in airlines['flights']:
        print("Flight ID: %s" % str(result['flight_id']))
        print("Flight number: %s" % str(result['flight_num']))
        print("Departue airport: %s" % str(result['dep_airport']))
        print("Destination airport: %s" % str(result['dest_airport']))
        print("Departue datetime: %s" % str(result['dep_datetime']))
        print("Arrival datetime: %s" % str(result['arr_datetime']))
        print("Duration: %s" % str(result['duration']))
        print("Price: %s" % str(result['price']))
        print("")
    print("")

    # 
    # for airline in airlines['company_list']:
    #
    #     r = requests.get(airline['url']+'/api/findflight/', headers={'content-type':'application/json'}, data=json.dumps(payload))
    #
    #         # check if the content is json
    #     # if(r.headers['Content-Type'] == 'application/json'):
    #     try:
    #         flights = r.json()
    #         print("")
    #         print("Airline provider --> %s" % (airline['company_code']))
    #         for result in flights['flights']:
    #             print("Flight ID: %s" % str(result['flight_id']))
    #             print("Flight number: %s" % str(result['flight_num']))
    #             print("Departue airport: %s" % str(result['dep_airport']))
    #             print("Destination airport: %s" % str(result['dest_airport']))
    #             print("Departue datetime: %s" % str(result['dep_datetime']))
    #             print("Arrival datetime: %s" % str(result['arr_datetime']))
    #             print("Duration: %s" % str(result['duration']))
    #             print("Price: %s" % str(result['price']))
    #             print("")
    #         print("")
    #
    #     except:
    #         if(r.headers['Content-Type'] == 'text/plain'):
    #             print("%s was unable to respond. (Error message: %s)" % (airline['url'],r.text))
    #             print("")
    #         else:
    #             print("Airline provider --> %s is not sending JSON or 'text/plain' not specified"  % (airline['url']))
    #             print("")


########################## PART 2 ################################

    print("")
    print("                 2. BOOKING FLIGHT                 ")
    print("")
    payload_list = []


    print("Introduce the correct parameters in order to succesfully complete the booking. ")
    print("Company name: ")
    company_name = input()

    print("Flight ID: ")
    flight_id = input()


    # try:
    #     company_name, flight_id = user_input.split(" ")
    # except:
    #     print("Wrong number of parameters")

    while num_passengers > 0:
        print("PLEASE INTRODUCE THE INFORMATION FOR THE %d PASSENGER (name, surname, email, phone)" % (num_passengers))
        num_passengers = num_passengers - 1
        user_input = input()
        try:
            first_name, surname, email, phone = user_input.split(" ")
            print(first_name)
        except ValueError:
            print("Please provide all the required parameters")

        print("These are the params provided: %s %s %s %s" % (first_name,  surname, email, phone))

        # for airline in airlines['company_list']:
        #     if airline['company_code'] == company_name:
        #         chosen_url = airline["url"]
        #
        #
        # print("You have chosen to buy from: %s" % chosen_url)


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

    # response_r = json.loads(r.text)
    r = requests.post(chosen_url+'/api/bookflight/', headers={'content-type':"application/json"}, data=json.dumps(passengers))
    print(r.status_code)
    # print(r.text)
    print("")
    if(r.headers['Content-Type'] == 'text/plain'):
        print("Error occured: %s", r.text)
    else:
        if(r.headers['Content-Type'] == 'application/json'):
            response_r = r.json()
            print(response_r)
            print("Booking confirmed!")
            print("Booking number: %s" % str(response_r["booking_num"]))
            print("Booking status: %s" % str(response_r["booking_status"]))
            print("Total price: %s" % str(response_r["tot_price"]))
            print("")
        else:
            print("Content-Type not specified by %s" % company_name)

#
#
#     # chosen_url = 'http://sc15sn.pythonanywhere.com'
#     # chosen_url = 'http://ggbusuioc.pythonanywhere.com'
    chosen_url = 'http://localhost:8000'
# # =====================================================================
# ########################### PART 3 ################################
#
    print("3. Request PAYMENT METHODS")


    r = requests.get(chosen_url+'/api/paymentmethods/', headers={'content-type':"application/json"})
    payment_providers = json.loads(r.text)
    print("PAYMENT PROVIDER ID | PAYMENT PROVIDER NAME")

    for result in payment_providers["pay_providers"]:
        print(str(result['pay_provider_id']) + " " + result['pay_provider_name'])

# ########################### PART 4 ################################
    print("")
    print("                 4. PAY FOR BOOKING                         ")
    print("")

    print("Introduce the correct parameters in order to succesfully complete the payment. ")
    print("Booking number: ")
    booking_num = input()

    print("Payment provider id: ")
    pay_provider_id = input()



    booking_payload = {}
    booking_payload['booking_num'] = booking_num
    booking_payload['pay_provider_id'] = pay_provider_id

    b = requests.post(chosen_url+ '/api/payforbooking/', headers={'content-type':"application/json"}, data=json.dumps(booking_payload))
    # print(json.loads(b.text))
    # print(b.text)
    print(b.url)
    print(b.status_code)
    print(b.headers)

    #
    # if(b.headers['Content-Type'] == 'text/plain'):
    #     print("Error occured: %s", b.text)
    # else:
    #     if((b.headers['Content-Type'] == 'application/json')):
    #         response = json.loads(b.text)
    #         print("REsponse")
    #         print(response)
    #     else:
    #         print("Content-Type not specified by %s" % (chosen_url))


    if(b.status_code == 503):
        print("Error occured: %s" % (b.text))
    else:
        if(b.status_code == 201):
            response = json.loads(b.text)
            print("REsponse")
            print(response)
        else:
            print(b.status_code)
            print("Bad response %s" % (chosen_url))


    # response = json.loads(b.text)
    # print("Response")
    # print(response)
    # print(" INVOICE ID | URL | PAY PROVIDER ID | BOOKING NUM")
    #
    #
    # print(str(response["invoice_id"]) + " " + str(response["pay_provider_id"]) + " " + response["url"] + " " + response["booking_num"] )
    # # print(b.text)

    # loging with personal account
    print("PLEASE ENTER YOUR PERSONAL USERNAME AND PASSWORD TO PAY FOR THE INVOICE")
    user_input = input()
    try:
        username, password = user_input.split(" ")
    except ValueError:
        print("Please provide all the required parameters")

    session = requests.session()
    b = session.post('http://sc15rmdc.pythonanywhere.com'+"/api/login/", headers={'content-type':"application/x-www-form-urlencoded"}, data = {'username':username,'password':password})

    print("Session")
    print(b.url)
    print(b.status_code)
    print("")
    payload = {}
    payload['payprovider_ref_num'] = str(response['invoice_id'])
    payload['client_ref_num'] = str(response["booking_num"])
    payload['amount'] = str(response_r["tot_price"])
    print(payload['amount'] + " " + payload['client_ref_num'] + " " + payload['payprovider_ref_num'])
    print(payload)

    f = session.post('http://sc15rmdc.pythonanywhere.com'+"/api/payinvoice/", headers={'Content-Type':"application/json"}, data = json.dumps(payload))
    print("Check if the invoice was paid")
    print(f.status_code)
    print(f.url)
    print(f.text)
    result = json.loads(f.text)
    print("Stamp: %s" % (result['stamp_code']))


# ########################### PART 5 ################################
#
    print("")
    print("                     5. FINALISE BOOKING                                               ")
    print("Please insert your BOOKING NUMBER, PAYMENT PROVIDER IDENTIFIER, PAYMENT PROVIDER ELECTRONIC STAMP")
    print("")

    user_input = input()
    try:
        booking_num, pay_provider_id, stamp = user_input.split(" ")
    except ValueError:
        print("Please provide all the required parameters")

    finalize_booking_payload = {}
    finalize_booking_payload['booking_num'] = booking_num
    finalize_booking_payload['pay_provider_id'] = pay_provider_id
    finalize_booking_payload['stamp'] = stamp

    ## print the overall

    b = requests.post(chosen_url+"/api/finalizebooking/", headers={'Content-Type':"application/json"}, data=json.dumps(finalize_booking_payload))

    print(b.status_code)
    print(b.text)
    print(json.loads(b.text))


    try:
        response = json.loads(b.text)
        print(response)
    except ValueError:
        print(b.text)




# ########################### PART 6 ################################
#
    print("BOOKING STATUS Part 6")
    print("Please insert your BOOKING NUMBER")
    user_input = input()
    try:
        booking_num = user_input
    except:
        print("Please provide all the required parameters")



    print(booking_num)
    status_payload = {}
    status_payload["booking_num"] = booking_num
    r = requests.get(chosen_url+'/api/bookingstatus/', headers={'Content-Type':"application/json"}, data=json.dumps(status_payload))
    print(r.status_code)
    print(r.text)
    # try:
    #     response = json.loads(r.text)
    #     print("BOOKING NUM | BOOKING STATUS | FLIGHT NUM | DEP AIRPORT | DEST AIRPORT | DEP DATETIME | ARR DATETIME | DURATION")
    #     print(response["booking_num"] + " " +response["booking_status"] + " " +response["flight_num"] + " " +response["dep_airport"] + " " +response["dest_airport"] + " " +response["dep_datetime"] + " " +response["arr_datetime"] + " " +response["duration"] )
    # except ValueError:
    #     print(r.text)
#


# ########################### PART 7 ################################
#
    print("CANCEL BOOKING Part 7")
    print("Please insert your BOOKING NUMBER")
    user_input = input()
    try:
        booking_num = user_input
    except:
        print("Please provide all the required parameters")
    cancel_payload = {}
    cancel_payload["booking_num"] = booking_num

    r = requests.post(chosen_url+'/api/cancelbooking/', headers={'Content-Type':"application/json"}, data=json.dumps(cancel_payload))

    try:
        response = json.loads(r.text)
        print("BOOKING NUMBER | BOOKING STATUS")
        print(response["booking_num"] + " " + response["booking_status"])
    except ValueError:
        print(r.text)

    break
    # process_complete = True







############################ PAYMENT OPTIONS ###############################
