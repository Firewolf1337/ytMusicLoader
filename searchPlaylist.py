from ytmusicapi import YTMusic
import os
import pathlib
import sys
import argparse

# If proxy is used uncomment this
#proxy = 'http://1.2.3.4:8080'
#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy

parser = argparse.ArgumentParser()
parser.add_argument('--artist', '-a', help="Name of the Artist to search for the albums", type= str)
parser.add_argument('--writemode', '-w', help="Append or overwrite the existing Playlist.txt - Options a for append or w overwrite", type= str, choices=['a', 'w'])
args = parser.parse_args()


path = pathlib.Path(__file__).parent.resolve()
ytmusic = YTMusic()
search_results = ytmusic.search(args.artist, 'albums')
albumPlaylistIds=[]
if len(search_results) > 0:
    print("Found following Album:", flush=True)
for art in search_results:
    album = ytmusic.get_album(art['browseId'])

    if album['type'] == "Album":
        released = True
        for track in album['tracks']:
            if not track['isAvailable']:
                released = False
        if released:
            print("\"" + album['title'] + "\" from Year " + str(album['year']) + " with " + str(album['trackCount']) + " Songs", flush=True)
            albumPlaylistIds.append(ytmusic.get_album(art['browseId'])['audioPlaylistId'])
        else:
            print("!!!! Skipping \"" + album['title'] + "\" from Year " + str(album['year']) + " because it is not relead completely !!!!!", flush=True)
with open(str(path) + '\\playlists.txt', args.writemode) as Playlists:
    for id in albumPlaylistIds:
        Playlists.write("https://music.youtube.com/playlist?list=" + id + "\n")



