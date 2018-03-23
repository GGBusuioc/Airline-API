import requests
import json
from bson import json_util
import datetime

dep_airport = "Leeds"
dest_airport = "Luton"
dep_date = "2018-03-01"
num_passengers = 1
is_flex = "N"



url = 'http://ggbusuioc.pythonanywhere.com/api/findflight/'
payload = {
    'dep_airport' : dep_airport,
    'dest_airport': dest_airport,
    'dep_date': dep_date,
    'num_passengers': num_passengers,
    'is_flex': is_flex,
}

r = requests.get(url, data=json.dumps(payload))
print(r.status_code)
print(r.text)
