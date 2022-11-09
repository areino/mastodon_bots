import requests
import json

## Coordinates for Madrid
town = "Madrid"
latitude = 40.4167
longitude = -3.7033

## Mastodon API config
token = ""
instance = "laterracita.online"

## Get weather info
url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&current_weather=true"

response = requests.request(method = "GET", url = url)
if response.status_code != 200:
    print("Error: " + response.content)
    exit(-1)

weather = response.json()

temperature = round(weather["current_weather"]["temperature"])
code = weather["current_weather"]["weathercode"]

if code == 0 or code == 1:
    desc = "Despejado."
elif code == 2 or code == 3:
    desc = "Nublado."
elif code == 45 or code == 48:
    desc = "Niebla."
elif (code >= 50 and code <=69) or (code >= 80 and code <=82):
    desc = "Llueve."
elif (code >= 70 and code <= 79) or (code >= 85 and code <=86):
    desc = "Nieva."
elif code >= 90 and code <= 100:
    desc = "Hay tormenta."
else:
    desc = "Hace un tiempo muy raro."

## Compose post
toot = desc + " " + str(temperature) + " grados. En " + town + "."

# Prepare Mastodon API call
url = "https://" + instance + "/api/v1/statuses"

headers =   {
            'Accept': 'application/json', 
            'Content-type': 'application/json', 
            'Authorization': 'Bearer ' + token
            }

data =      {  'status': toot  }


## Toot it
response = requests.request(method = "POST", url = url, data = json.dumps(data), headers = headers)

