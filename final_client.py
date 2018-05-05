import requests
import json
from bson import json_util
import datetime


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


print("******************************************************************************************")
print("***                  Choose one path: 1. Airline   2. Payment                          ***")
print("******************************************************************************************")

print("Path option (1 or 2)")
pathOption = input()

while True:

    if(pathOption == "1"):
        print("******************************************************************************************")
        print("***                             Airline Menu                                           ***")
        print("******************************************************************************************")

        print("")
        print("                 1. FIND FLIGHTS                  ")
        print("")
        #
        #
        # print("Departue airport: ")
        # dep_airport = input()
        #
        # print("Destination airport: ")
        # dest_airport = input()
        #
        # print("Departue datetime (YYYY-MM-DD): ")
        # dep_date = input()
        #
        # print("Num paggengers: ")
        # num_passengers = input()
        #
        # print("Flexible (y/n): ")
        # is_flex = input()


        dep_airport = "LBA"
        dest_airport = "MAN"
        dep_date = "2018-03-17"
        num_passengers = 2
        is_flex = 'y'

        url = 'http://directory.pythonanywhere.com/api/list/'
        payload = {'company_type': "airline",}
        r = requests.get(url, headers={'content-type':'application/json'}, data=json.dumps(payload))

        payload = {
            'dep_airport' : dep_airport,
            'dest_airport': dest_airport,
            'dep_date': dep_date,
            'num_passengers': num_passengers,
            'is_flex': is_flex,
        }

        airlines = json.loads(r.text)


        for airline in airlines['company_list']:

            r = requests.get(airline['url']+'/api/findflight/', headers={'content-type':'application/json'}, data=json.dumps(payload))

            try:
                flights = r.json()
                print("")
                print("Airline provider --> %s" % (airline['company_code']))
                for result in flights['flights']:
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

            except:
                if(r.status_code==503):
                    print("%s was unable to respond. (Error message: %s)" % (airline['url'],r.text))
                    print("")
                else:
                    print("Airline provider --> %s is not sending JSON or 'text/plain' not specified"  % (airline['url']))
                    print("")





        print("")
        print("                 2. BOOKING FLIGHT                 ")
        print("")

        payload_list = []

        print("Company name: ")
        company_name = input()

        print("Flight ID: ")
        flight_id = input()


        for airline in airlines['company_list']:
            if airline['company_code'] == company_name:
                chosen_url = airline["url"]

        print("You have chosen to buy from: %s" % chosen_url)


        print(num_passengers)
        print(type(num_passengers))

        # for all the passengers
        while int(num_passengers) > 0:

            print("PLEASE INTRODUCE THE INFORMATION FOR PASSENGER  %d (name, surname, email, phone)" % (int(num_passengers)))
            num_passengers = num_passengers - 1
            user_input = input()
            try:
                first_name, surname, email, phone = user_input.split(" ")
                print(first_name)
            except ValueError:
                print("Please provide all the required parameters")

            print("These are the params provided: %s %s %s %s" % (first_name,  surname, email, phone))



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

        r = requests.post(chosen_url+'/api/bookflight/', headers={'content-type':"application/json"}, data=json.dumps(passengers))
        print("")
        if(r.status_code == 503):
            print("Error occured: %s", r.text)
        else:
            if(r.status_code == 201):
                response_r = r.json()
                print("Booking confirmed!")
                print("Booking number: %s" % str(response_r["booking_num"]))
                print("Booking status: %s" % str(response_r["booking_status"]))
                print("Total price: %s" % str(response_r["tot_price"]))
                print("")
            else:
                print("Bad status code %s" % company_name)

        print("")
        print("                 3. REQUEST MAYMENT METHODS        ")
        print("")

        r = requests.get(chosen_url+'/api/paymentmethods/', headers={'content-type':"application/json"})
        payment_providers = json.loads(r.text)
        print("PAYMENT PROVIDER ID | PAYMENT PROVIDER NAME")

        for result in payment_providers["pay_providers"]:
            print(str(result['pay_provider_id']) + " " + result['pay_provider_name'])


        print("")
        print("                 4. PAY FOR BOOKING                 ")


        print("Introduce the correct parameters in order to succesfully complete the payment. ")
        print("Booking number: ")
        booking_num = input()

        print("Payment provider id: ")
        pay_provider_id = input()


        booking_payload = {}
        booking_payload['booking_num'] = booking_num
        booking_payload['pay_provider_id'] = pay_provider_id

        b = requests.post(chosen_url+ '/api/payforbooking/', headers={'content-type':"application/json"}, data=json.dumps(booking_payload))


        if(b.status_code == 503):
            print("Error occured: %s" % (b.text))
        else:
            if(b.status_code == 201):
                response = json.loads(b.text)
                print("Please continue")
            else:
                print(b.status_code)
                print("Bad response %s" % (chosen_url))




        print("PLEASE ENTER YOUR PERSONAL USERNAME AND PASSWORD TO PAY FOR THE INVOICE (username password)")
        user_input = input()
        try:
            username, password = user_input.split(" ")
        except ValueError:
            print("Please provide all the required parameters")

        session = requests.session()
        try:
            b = session.post('http://sc15rmdc.pythonanywhere.com'+"/api/login/", headers={'content-type':"application/x-www-form-urlencoded"}, data = {'username':username,'password':password})
        except:
            print("Account not found. EXIT")


        print("")
        payload = {}
        payload['payprovider_ref_num'] = str(response['invoice_id'])
        payload['client_ref_num'] = str(response["booking_num"])
        payload['amount'] = str(response_r["tot_price"])
        print(payload['amount'] + " " + payload['client_ref_num'] + " " + payload['payprovider_ref_num'])



        f = session.post('http://sc15rmdc.pythonanywhere.com'+"/api/payinvoice/", headers={'Content-Type':"application/json"}, data = json.dumps(payload))
        print("Check if the invoice was paid")

        result = json.loads(f.text)
        print("Stamp: %s" % (result['stamp_code']))




        print("")

        print("")
        print("                 5. FINALISE BOOKING                ")
        print("")
        print("Please insert your BOOKING NUMBER, PAYMENT PROVIDER IDENTIFIER, PAYMENT PROVIDER ELECTRONIC STAMP")


        user_input = input()
        try:
            booking_num, pay_provider_id, stamp = user_input.split(" ")
        except ValueError:
            print("Please provide all the required parameters")
            sys.exit()

        finalize_booking_payload = {}
        finalize_booking_payload['booking_num'] = booking_num
        finalize_booking_payload['pay_provider_id'] = pay_provider_id
        finalize_booking_payload['stamp'] = stamp


        b = requests.post(chosen_url+"/api/finalizebooking/", headers={'Content-Type':"application/json"}, data=json.dumps(finalize_booking_payload))

        try:
            response = json.loads(b.text)
            print("BOOKING NUMBER | BOOKING STATUS")
            print(response["booking_num"] + " " + response["booking_status"])
        except ValueError:
            print(b.text)


        print("")
        print("                 6. BOOKING STATUS               ")
        print("")


        print("Please insert your BOOKING NUMBER")
        user_input = input()
        try:
            booking_num = user_input
        except:
            print("Please provide all the required parameters")

        status_payload = {}
        status_payload["booking_num"] = booking_num
        r = requests.get(chosen_url+'/api/bookingstatus/', headers={'Content-Type':"application/json"}, data=json.dumps(status_payload))
        try:
            response = json.loads(r.text)
            print("BOOKING NUMBER | BOOKING STATUS")
            print(response["booking_num"] + " " + response["booking_status"])
        except ValueError:
                print(r.text)


        print("")
        print("                 7. CANCEL BOOKING                ")
        print("")


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

        print("Path option (1 or 2)")
        pathOption = input()

    if(pathOption == "2"):

        url = 'http://directory.pythonanywhere.com/api/list/'
        payload = {'company_type': "payment",}
        r = requests.get(url, headers={'content-type':'application/json'}, data=json.dumps(payload))

        pp = json.loads(r.text)
        company_codes = []
        for payment in pp['company_list']:
            print("Company code: %s" % (payment['company_code']))
            print("Company name: %s" % (payment['company_name']))
            company_codes.append(payment['company_code'])
            print("")

        flag = False

        while(flag==False):

            print("Choose a company code from the above")
            the_one = input()

            # Check if the user inserted a valid option
            for elem in company_codes:
                if elem == the_one:
                    flag = True


        for payment in pp['company_list']:
            if payment['company_code'] == the_one:
                the_url = payment['url']
                the_company = payment['company_name']


        session = requests.session()

        print("******************************************************************************************")
        print("***                             Payment Menu                                           ***")
        print("******************************************************************************************")
        print("")
        print(" 1 - REGISTER  2 - LOG IN   3 - LOG OUT")
        print(" 4 - NEW ACCOUNT  5 - DEPOSIT   6 - TRANSFER")
        print(" 7 - BALANCE  8 - CREATE INVOICE   9 - PAY INVOICE")
        print(" 10 - STATEMENT                   0 - EXIT MENU")
        print("")



        print("Choose an option from the menu")
        option = input()

        while(option != "0"):

            if(option=="1"):
                print("           1. REGISTER             ")

                print("First name: ")
                first_name = input()
                print("Surname: ")
                surname = input()
                print("Email: ")
                email = input()
                print("Phone: ")
                phone = input()
                print("Username: ")
                username = input()
                print("Password: ")
                password = input()
                print("Personal or Business? ")
                customer_type = input()

                payload = {}
                payload['first_name'] = first_name
                payload['surname'] = surname
                payload['email'] = email
                payload['phone'] = phone
                payload['username'] = username
                payload['password'] = password
                payload['customer_type'] = customer_type


                b = requests.post(the_url+ '/api/register/', headers={'content-type':"application/json"}, data=json.dumps(payload))


                if(b.status_code == 201 or b.status_code == 503):
                    print(b.text)
                else:
                    print("ERROR %s" % (b.status_code))

            if(option == "2"):
                print("           2. LOG IN             ")
                print("Username: ")
                username = input()
                print("Password: ")
                password = input()


                payload = {}
                payload['username'] = username
                payload['password'] = password

                b = session.post(the_url+ '/api/login/', headers={'content-type':"application/x-www-form-urlencoded"}, data = {'username':username,'password':password})


                if(b.status_code == 200):
                    print(b.text)
                else:
                    print("ERROR %s" % (b.status_code))

            if(option == "3"):
                print("           3. LOG OUT             ")

                b = session.post(the_url+ '/api/logout/', headers={'content-type':"application/x-www-form-urlencoded"})


                if(b.status_code == 200):
                    print(b.text)
                else:
                    print("ERROR %s" % (b.status_code))

            if(option=="4"):
                print("           4. CREATE NEW ACCOUNT             ")
                b = session.post(the_url+ '/api/newaccount/',  headers={'content-type':"application/x-www-form-urlencoded"})


                if(b.status_code == 201 or b.status_code == 503):
                    print(b.text)
                else:
                    print("ERROR %s" % (b.status_code))



            if(option=="5"):
                print("           5. DEPOSIT            ")
                print("Amount: ")
                amount = input()
                print("Account number: ")
                account_num = input()

                payload = {}
                payload['amount'] = amount
                payload['account_num'] = account_num

                b = session.post(the_url+ '/api/deposit/',   headers={'content-type':"application/json"}, data=json.dumps(payload))


                if(b.status_code == 201):
                    payload = json.loads(b.text)

                    print("Account num: %s" % (payload["account_num"]))
                    print("Balance: %s" % (payload["balance"]))
                else:
                    if(b.status_code == 503):
                        print(b.text)
                    else:
                        print("ERROR %s" % (b.status_code))


            if(option == "6"):
                print("           6. TRANSFER             ")
                print("Amount: ")
                amount = input()
                print("From acccount number: ")
                from_account = input()
                print("To acccount number: ")
                to_account = input()


                payload = {}
                payload['amount'] = amount
                payload['from_account_num'] = from_account
                payload['to_account_num'] = to_account


                b = session.post(the_url+ '/api/transfer/',   headers={'content-type':"application/json"}, data=json.dumps(payload))


                if(b.status_code == 201):
                    payload = json.loads(b.text)
                    print("Account number from where money were taken from: %s" % (payload['account_num']))
                    print("Balance: %s" % (payload['balance']))
                else:
                    if(b.status_code == 503):
                        print(b.text)
                    else:
                        print("ERROR %s" % (b.status_code))



            if(option == "7"):
                print("           7. BALANCE             ")

                b = session.get(the_url+ '/api/balance/')
                if(b.status_code == 200):
                    payloadx = json.loads(b.text)
                    payload = payloadx['accounts']
                    for account in payload:
                        print("Account number: %s" % account['account_num'])
                        print("Balance: %s" % account['balance'])
                else:
                    if(b.status_code == 503):
                        print(b.text)
                    else:
                        print("ERROR %s" % (b.status_code))
                        print(b.text)

            if(option == "8"):
                print("           8. CREATE INVOICE             ")

                print("Account number: ")
                account_num = input()
                print("Client reference number(?): ")
                client_ref_num = input()
                print("Amount: ")
                amount = input()

                payload = {}
                payload['account_num'] = account_num
                payload['client_ref_num'] = client_ref_num
                payload['amount'] = amount

                print(payload)

                b = session.post(the_url+ '/api/createinvoice/',   headers={'content-type':"application/json"}, data=json.dumps(payload))
                if(b.status_code == 201):
                    payload = json.loads(b.text)
                    print("Payprovider ref number: %s" % (payload['payprovider_ref_num']))
                    print("Stamp: %s" % (payload['stamp_code']))
                else:
                    if(b.status_code == 503):
                        print(b.text)
                    else:
                        print("ERROR %s" % (b.status_code))

            if(option == "9"):
                print("           9. PAY INVOICE             ")

                print("Payprovider reference number: ")
                payprovider_ref_num = input()
                print("Client reference number(?): ")
                client_ref_num = input()
                print("Amount: ")
                amount = input()

                payload = {}
                payload['payprovider_ref_num'] = payprovider_ref_num
                payload['client_ref_num'] = client_ref_num
                payload['amount'] = amount

                b = session.post(the_url+ '/api/payinvoice/',   headers={'content-type':"application/json"}, data=json.dumps(payload))
                if(b.status_code == 201):
                    payload = json.loads(b.text)
                    print("Stamp: %s" % (payload['stamp_code']))
                else:
                    if(b.status_code == 503):
                        print(b.text)
                    else:
                        print("ERROR %s" % (b.status_code))

            if(option == "10"):
                print("           10. STATEMENT             ")

                print("Account number: ")
                account_num = input()

                payload = {}
                payload['account_num'] = account_num

                b = session.get(the_url+ '/api/statement/',   headers={'content-type':"application/json"}, data=json.dumps(payload))
                if(b.status_code == 201):
                    payload = json.loads(b.text)
                    for transaction in payload["transactions"]:
                        print("Transaction date: %s" % (transaction['date']))
                        print("Reference number of the transaction: %s" % (transaction['reference']))
                        print("Amount: %s" % (transaction['amount']))

                else:
                    if(b.status_code == 503):
                        print(b.text)
                    else:
                            print("ERROR %s" % (b.status_code))
            print("******************************************************************************************")
            print("***                             Payment Menu                                           ***")
            print("******************************************************************************************")
            print("")
            print(" 1 - REGISTER  2 - LOG IN   3 - LOG OUT")
            print(" 4 - NEW ACCOUNT  5 - DEPOSIT   6 - TRANSFER")
            print(" 7 - BALANCE  8 - CREATE INVOICE   9 - PAY INVOICE")
            print(" 10 - STATEMENT                   0 - EXIT MENU")
            print("")
            # Ask the user for the next imput
            print("Choose an option from the menu")
            option = input()

        print("Path option (1 or 2)")
        pathOption = input()
