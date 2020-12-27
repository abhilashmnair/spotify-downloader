artist = []
def get_artists(data):
    artists = data['album']['artists']
    for item in artists:
        artist.append(item['name'])
    return artist

def get_album_art(data):
    imageUrl = data['album']['images'][0]['url']
    return imageUrl