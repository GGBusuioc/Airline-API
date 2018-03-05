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
        dep_airport, dest_airport, dep_date, num_passengers, is_flex = user_input.split(" ")
    except ValueError:
        print("Please provide all the required parameters")


    #print("This is your json object: " + json_str)
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
        flights = json.loads(r.json(), object_hook=json_util.object_hook)
        print("*************************************")
        print("FLIGHT ID | FLIGHT NR | DEP AIR | DEST AIR | DEP D&T | ARI D&T | DURATION [H, M] | PRICE £")
        print("\n")
        for result in flights:
            for field in result:
                if(type(field)!=datetime.datetime):
                    print("%s |" % (field), end=" ")
                else:
                    print("%d/%d/%d H:%d M:%d |" % (field.year, field.month, field.day, field.hour, field.minute), end=" ")
            print("\n")
        print("*************************************")


    except ValueError:
        print("Nothing was found. A reason plus the payload. ")
