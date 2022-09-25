    #  http://api.open-notify.org/astros.json
    #  vanuit browser
    # {"message": "success", "people": [{"craft": "ISS", "name": "Oleg Ortemyev"}, {"craft": "ISS", "name": "Denis Matveev"}, etc, "number": 13}

import requests

response = requests.get ('http://api.open-notify.org/astros.json')

json= response.json()

print (json)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

for p in json['people']:
    print(p.get('name'))

for p in json['people']:
    print(p.get('name'),'CRAFT: ',  p.get('craft'))
    
# print (astros)



