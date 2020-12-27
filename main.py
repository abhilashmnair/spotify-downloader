import requests
import base64
import json
from secrets import *
from definitions import *
from urllib.request import urlopen

url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

message = f"{clientId}:{clientSecret}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')


headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']

headers = {
    "Authorization": "Bearer " + token
}

userQuery = input('Enter track title and artist / Spotify URL : ')

if 'open.spotify.com' in userQuery:
    trackId = userQuery.split('/')[4]
else:
    query = '+'.join(str(val) for val in userQuery.split(' '))
    requestUrl = f"https://api.spotify.com/v1/search?q={query}&type=track"
    response = requests.get(url=requestUrl, headers=headers)
    data = response.json()
    trackId = data['tracks']['items'][0]['id']

requestUrl = f"https://api.spotify.com/v1/tracks/{trackId}"

response = requests.get(url=requestUrl, headers=headers)
#print(json.dumps(response.json(), indent=2))

data = response.json()
print(get_title(data))
print(get_artists(data))
print(get_album_artists(data))
print(get_album_name(data))
print(get_release_year(data))