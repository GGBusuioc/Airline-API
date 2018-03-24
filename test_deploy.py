import requests
import json
from bson import json_util
import datetime

dep_airport = "Leeds"
dest_airport = "Luton"
dep_date = "2018-03-01"
num_passengers = 1
is_flex = "N"



#url = 'http://ggbusuioc.pythonanywhere.com/api/findflight/'
url = 'http://directory.pythonanywhere.com/api/list/'
# payload = {
#     'dep_airport' : dep_airport,
#     'dest_airport': dest_airport,
#     'dep_date': dep_date,
#     'num_passengers': num_passengers,
#     'is_flex': is_flex,
# }
payload = {
    'company_type': "payment"
}
print(json.dumps(payload))


r = requests.get(url, headers={'content-type':"application/json"}, data=json.dumps(payload))


print(r.status_code)
print(r.text)
url = 'http://directory.pythonanywhere.com/api/register/'
payload = {
    'company_name': "George Busuioc Airlines Ltd",
    'company_type': "airline",
    'url': "http://ggbusuioc.pythonanywhere.com/",
    'company_code': "GGB"
}
b = requests.post(url, headers={'content-type':"application/json"}, data=json.dumps(payload))
print(b.status_code)
