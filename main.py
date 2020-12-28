import asyncio
import requests
import json
import shutil
from definitions import *
from os.path import join, exists
from PIL import Image
from youtube_search import YoutubeSearch
from pytube import YouTube

tokenUrl = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

headers['Authorization'] = f"Basic {generate_code()}"
data['grant_type'] = "client_credentials"

r = requests.post(tokenUrl, headers=headers, data=data)

token = r.json()['access_token']

headers = { "Authorization": "Bearer " + token }

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

data = response.json()
trackTitle = get_title(data)
trackArtists = get_artists(data)
print(get_album_artists(data))
print(get_album_name(data))
print(get_release_year(data))

results = YoutubeSearch(f"{trackTitle}+{trackArtists}", max_results=10).to_dict()

youtubeSongUrl = 'https://youtube.com/' + str(results[0]['url_suffix'])

convertedFileName = f'{trackArtists} - {trackTitle}'
convertedFilePath = join('.', convertedFileName) + '.mp3'

yt = YouTube(youtubeSongUrl)
trackAudioStream = yt.streams.get_audio_only()

downloadedFilePath = trackAudioStream.download(output_path='./Temp',filename=convertedFileName,skip_existing=False)

if downloadedFilePath is None:
    return 'Download Error'

command = 'ffmpeg -v quiet -y -i "%s" -acodec libmp3lame -abr true ' \
          '-af "apad=pad_dur=2, dynaudnorm, loudnorm=I=-17" "%s"'
formattedCommand = command % (downloadedFilePath, convertedFilePath)
process = await asyncio.subprocess.create_subprocess_shell(formattedCommand)
_ = await process.communicate()

while True:
    if exists(convertedFilePath):
        break

