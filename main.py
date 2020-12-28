import requests
import json
import os
from definitions import *
from os.path import join, exists
from os import mkdir, remove
from mutagen.easyid3 import EasyID3, ID3
from mutagen.id3 import APIC as AlbumCover
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

search_song(q):
    if 'open.spotify.com' in q:
        return q.split('/')[4]
    else:
        query = '+'.join(str(val) for val in q.split(' '))
        requestUrl = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(url=requestUrl, headers=headers)
        data = response.json()
        return data['tracks']['items'][0]['id']

trackId = search_song(userQuery)
if None in trackId:
    print('Song not found in Spotify Database! Searching in YouTube...')

requestUrl = f"https://api.spotify.com/v1/tracks/{trackId}"
response = requests.get(url=requestUrl, headers=headers)
data = response.json()

print('Title : ' + get_title(data))
print('Artists : ' + get_artists(data))
print('Album : ' + get_album_name(data))

albumArt = get_album_art(data)
trackTitle = get_title(data)
trackArtists = get_artists(data)
albumName = get_album_name(data)
release_date = get_release_year(data)
trackNumber = get_track_number(data)
discNumber = get_disc_number(data)

results = YoutubeSearch(f"{trackTitle}+{trackArtists}", max_results=10).to_dict()
youtubeSongUrl = 'https://youtube.com/' + str(results[0]['url_suffix'])

albumArtists = get_album_artists(data)
convertedFileName = f'{albumArtists}-{trackTitle}'
convertedFilePath = join('.',convertedFileName) + '.mp3'

if exists(convertedFilePath):
    print('Already exists!')

yt = YouTube(youtubeSongUrl)
downloadedFilePath = yt.streams.get_audio_only().download(filename=convertedFileName,skip_existing=False)

print('\nDownloaded file location : ' + downloadedFilePath)

#FFMPEG converting
command = f'ffmpeg -v quiet -y -i "{downloadedFilePath}" -abr true -af "apad=pad_dur=2, dynaudnorm, loudnorm=I=-17" -vn -b:a 320k "{convertedFilePath}"'
result = os.system(command)

while

audioFile = EasyID3(convertedFilePath)
audioFile.delete()

#Saving track info fetched from Spotify
audioFile['title'] = trackTitle
audioFile['tracknumber'] = str(trackNumber)
audioFile['artist'] = trackArtists
audioFile['album'] = albumName
audioFile['albumartist'] = albumArtists
audioFile['originaldate'] = release_date
audioFile.save(v2_version=3)

#Saving AlbumArt
audioFile = ID3(convertedFilePath)
audioFile['APIC'] = AlbumCover(encoding=3,mime='image/jpeg',type=3,desc='Album Art',data=albumArt)
audioFile.save(v2_version=3)

#remove unwanted YouTube downloads
remove(downloadedFilePath)