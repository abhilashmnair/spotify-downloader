from datetime import datetime
from urllib.request import urlopen
from args import *
import json
import base64
import requests

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

def getLyricsUrl(title,artists):
    url = f'https://api.genius.com/search?q={title}+{artists}&access_token={geniusToken}'
    response = requests.get(url)
    data = response.json()
    try:
        lyricsUrl = data['response']['hits'][0]['result']['path']
        return lyricsUrl
    except IndexError:
        print('Lyrics not found. Skipping...')