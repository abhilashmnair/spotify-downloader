import requests
import base64
import json
from secrets import *

# Step 1 - Authorization 
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

# Encode as Base64
message = f"{clientId}:{clientSecret}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')


headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']

# Step 2 - Use Access Token to call playlist endpoint

trackId = '0IHSAULL6jRYaDURDyVY12'
playlistUrl = f"https://api.spotify.com/v1/tracks/{trackId}"
headers = {
    "Authorization": "Bearer " + token
}

response = requests.get(url=playlistUrl, headers=headers)
#print(json.dumps(response.json(), indent=2))

data = response.json()
#print(data)
artist = data['album']['artists']
for item in artist:
    print(item['name'])