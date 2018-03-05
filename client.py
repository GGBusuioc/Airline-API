import requests
import json
from bson import json_util
import datetime
#from bson.codec_options import CodecOptions
print("Welcome to the client!")

process_complete = False

while process_complete == False:

    #print("=====================================")
    print("1. Find a flight")
    action = 'findflight'
    print("Pick a DEPARTUE AIRPORT,  DESTINATION AIPORT, DATE (YYYY-MM-DD), NUMBER OF PASSENGERS, FLEXIBLE (Y or N only)")
    user_input = input()
    # /findflight/departue_airport/destination_airport/date/
    try:
        departue, destination, date, number_of_tickets, is_flexible = user_input.split(" ")
    except ValueError:
        print("Please provide all the required parameters")


    #print("This is your json object: " + json_str)
    url = 'http://localhost:8000/findflight/'
    payload = {
        'departue_airport' : departue,
        'destination_airport': destination,
        'date': date,
        'number_of_tickets': number_of_tickets,
        'is_flexible': is_flexible,
    }

    r = requests.get(url, data=json.dumps(payload))

    try:
        flights = json.loads(r.json(), object_hook=json_util.object_hook)
        print("*************************************")
        for result in flights:
            for field in result:
                if(type(field)!=datetime.datetime):
                    print(field, end=" ")
                else:
                    print("%d/%d/%d at %d and %d minutes" % (field.year, field.month, field.day, field.hour, field.minute))
            print("\n")
        print("*************************************")
        # s = field
        # print(s)
        # s.strftime('%m/%d/%Y')
        # print(s)

    except ValueError:
        print("Nothing was found. A reason plus the payload. ")
