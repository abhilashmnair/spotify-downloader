from datetime import datetime
from urllib.request import urlopen
from secrets import *
import base64

def generate_code():
    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    return base64Bytes.decode('ascii')

def get_album_art(data):
    imageUrl = data['album']['images'][0]['url']
    rawAlbumArt = urlopen(imageUrl).read()
    return rawAlbumArt

def get_title(data):
    return data['name']

def get_album_artists(data):
    album_artists = []
    for item in data['album']['artists']:
        album_artists.append(item['name'])
    return ', '.join(str(val) for val in album_artists)

def get_artists(data):
    artists = []
    for item in data['artists']:
        artists.append(item['name'])
    return ', '.join(str(val) for val in artists)

def get_album_name(data):
    return data['album']['name']

def get_track_number(data):
    return data['track_number']

def get_disc_number(data):
    return data['disc_number']

def get_release_year(data):
    date = data['album']['release_date']
    year = date.split('-')
    return year[0]