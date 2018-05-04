import requests
import json
from bson import json_util
import datetime



# #
# url = 'http://directory.pythonanywhere.com/api/list/'
#
#
# payload = {
#     'company_type': "payment",
# }
#
# r = requests.get(url, headers={'content-type':'application/json'}, data=json.dumps(payload))

# print(r.text)
the_url = 'http://sc15rmdc.pythonanywhere.com'

# the_url = 'http://georgekom.pythonanywhere.com'

# the_url = 'http://zoltanszabo.pythonanywhere.com'



session = requests.session()

while True:
    print("")
    print("                  MENU                 ")
    print("")
    print(" 1 - REGISTER  2 - LOG IN   3 - LOG OUT")
    print(" 4 - NEW ACCOUNT  5 - DEPOSIT   6 - TRANSFER")
    print(" 7 - BALANCE  8 - CREATE INVOICE   9 - PAY INVOICE")
    print(" 10 - STATEMENT ")
    print("")

    print("Choose your action")
    option = input()
    if(option == "1"):
        print("           1. REGISTER             ")

        # print("First name: ")
        # first_name = input()
        # print("Surname: ")
        # surname = input()
        # print("Email: ")
        # email = input()
        # print("Phone: ")
        # phone = input()
        # print("Username: ")
        # username = input()
        # print("Password: ")
        # password = input()
        # print("Personal or Business? ")
        # customer_type = input()

        first_name = "George"
        surname = "Busuioc"
        email = "george.busuioc@gmail.com"
        phone = "0123456789"
        username = "ggb.business"
        password = "password123"
        customer_type = "business"

        payload = {}
        payload['first_name'] = first_name
        payload['surname'] = surname
        payload['email'] = email
        payload['phone'] = phone
        payload['username'] = username
        payload['password'] = password
        payload['customer_type'] = customer_type


        print(json.dumps(payload))


        b = requests.post(the_url+ '/api/register/', headers={'content-type':"application/json"}, data=json.dumps(payload))

        print("result")
        print(b.status_code)
        print(b.text)


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

        print(b.text)

    if(option == "3"):

        b = session.post(the_url+ '/api/logout/', headers={'content-type':"application/x-www-form-urlencoded"})

        if(b.status_code == 200):
            print(b.text)
        else:
            print(b.status_code)
            print(b.text)




    if(option=="4"):
        print("           4. CREATE NEW ACCOUNT             ")
        b = session.post(the_url+ '/api/newaccount/',  headers={'content-type':"application/x-www-form-urlencoded"})
        print(b.status_code)
        if(b.status_code == 201):
            print(b.text)

        else:
            if(b.status_code == 503):
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



        print(b.status_code)
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
        print(b.status_code)
        # print(b.text)
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
            print(b.text)
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
                print(b.text)


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
                # print(b.text)



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


            # print("Stamp: %s" % (payload['stamp_code']))
        else:
            if(b.status_code == 503):
                print(b.text)
            else:
                print("ERROR %s" % (b.status_code))
                # print(b.text)
