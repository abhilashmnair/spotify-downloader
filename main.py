import requests
import json
import os
from definitions import *
from args import *
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


#Some function definitions

def search_song(q):
    if 'open.spotify.com' in q:
        return q.split('/')[4]
    else:
        query = '+'.join(str(val) for val in q.split(' '))
        requestUrl = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(url=requestUrl, headers=headers)
        data = response.json()
        try:
            return data['tracks']['items'][0]['id']
        except:
            return None

def downloadViaSpotify(headers,trackId):
    requestUrl = f"https://api.spotify.com/v1/tracks/{trackId}"
    response = requests.get(url=requestUrl, headers=headers)
    data = response.json()

    print('Title : ' + get_title(data))
    print('Artists : ' + get_artists(data))
    print('Album : ' + get_album_name(data))

    results = YoutubeSearch(f"{get_title(data)}+{get_artists(data)}", max_results=10).to_dict()
    youtubeSongUrl = 'https://youtube.com/' + str(results[0]['url_suffix'])

    convertedFileName = f'{get_album_artists(data)}-{get_title(data)}'
    convertedFilePath = join('.',convertedFileName) + '.mp3'

    if exists(convertedFilePath):
        print('\nAlready downloaded!')
        quit()
    else:
        print('\nDownloading...')
    
        yt = YouTube(youtubeSongUrl)
        downloadedFilePath = yt.streams.get_audio_only().download(filename=convertedFileName,skip_existing=False)
        return convertedFilePath,downloadedFilePath,data

def downloadFromYoutube(q):
    results = YoutubeSearch(q, max_results=10).to_dict()
    youtubeSongUrl = 'https://youtube.com/' + str(results[0]['url_suffix'])
    trackTitle =  results[0]['title']

    convertedFilePath = join('.',trackTitle) + '.mp3'

    if exists(convertedFilePath):
        print('\nAlready downloaded!')
        quit()
    else:
        print('\nDownloading...')
    
        yt = YouTube(youtubeSongUrl)
        downloadedFilePath = yt.streams.get_audio_only().download(filename=trackTitle,skip_existing=False)
        print(f'Conerting to mp3 with {bitrate}kpbs bitrate..')
        command = f'ffmpeg -v quiet -y -i "{downloadedFilePath}" -acodec libmp3lame -abr true -af "apad=pad_dur=2" -vn -sn -dn -b:a {bitrate}k "{convertedFilePath}"'
        os.system(command)

        audioFile = EasyID3(convertedFilePath)
        audioFile.delete()
        audioFile['title'] = trackTitle
        audioFile.save(v2_version=3)
        remove(downloadedFilePath)

def saveMP3(downloadedFilePath,convertedFilePath,data):

    print(f'Conerting to mp3 with {bitrate}kpbs bitrate..')
    #FFMPEG Conversion
    command = f'ffmpeg -v quiet -y -i "{downloadedFilePath}" -acodec libmp3lame -abr true -af "apad=pad_dur=2" -vn -sn -dn -b:a {bitrate}k "{convertedFilePath}"'
    os.system(command)

    audioFile = EasyID3(convertedFilePath)
    audioFile.delete()

    #Saving track info fetched from Spotify
    audioFile['title'] = get_title(data)
    audioFile['tracknumber'] = str(get_track_number(data))
    audioFile['artist'] = get_artists(data)
    audioFile['album'] = get_album_name(data)
    audioFile['albumartist'] = get_album_artists(data)
    audioFile['originaldate'] = str(get_release_year(data))
    audioFile.save(v2_version=3)

    #Saving AlbumArt
    audioFile = ID3(convertedFilePath)
    audioFile['APIC'] = AlbumCover(encoding=3,mime='image/jpeg',type=3,desc='Album Art',data=get_album_art(data))
    audioFile.save(v2_version=3)

    #remove unwanted YouTube downloads
    remove(downloadedFilePath)

#Main program
userQuery = input('Enter track title and artist / Spotify URL : ')
trackId = search_song(userQuery)

if trackId is None:
    print('Song not found in Spotify Database! Searching in YouTube...')
    downloadFromYoutube(userQuery)
else:
    convertedFilePath,downloadedFilePath,data = downloadViaSpotify(headers,trackId)
    saveMP3(downloadedFilePath,convertedFilePath,data)

print(f'\nSaved in current directory.')
print('\n---------------------------------------------------------------------------')
print('\nHappy Hearing')
