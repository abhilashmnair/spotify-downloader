from datetime import datetime

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

def get_release_year(data):
    date = data['album']['release_date']
    year = date.split('-')
    return year[0]


