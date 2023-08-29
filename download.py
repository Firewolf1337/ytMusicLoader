from pytube import YouTube,Playlist
import pathlib
import sys
import subprocess
import musicbrainzngs as mbz 
from difflib import SequenceMatcher
import os
from mutagen.flac import FLAC
import re
import threading


# If proxy is used uncomment this
#proxy = 'http://1.2.3.4:80'
#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy


path = pathlib.Path(__file__).parent.resolve()

urls = []
if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg.startswith("http"):
            urls.append(arg)
else:
    with open(str(path) + '\\playlists.txt', "r") as Playlists:
        urls = Playlists.readlines()

print(urls)

special_characters=['<','>',':','|','&','(',')','*','\\','/', '?', '\"']
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def encode(param, name, inputfile):
    print("Start encoding ", name)
    subprocess.call(param)
    os.remove(inputfile)

for url in urls:
    print(url)
    p = Playlist(url=url)
    album = (p.title).replace('Album - ', '')
    artist = (p.videos[0]).author
    print("##################################################################################")
    print("    Downloading " + album + " from " + artist)
    print("    to \"" +  str(path) + "\\" + artist + "\\" + album + "\"")
    print("----------------------------------------------------------------------------------")
    counter = 0
    for yt in p.videos:
        counter = counter + 1
        print("Loading \"" + yt.title + "\" " + str(counter) + "/" + str(p.length))
        album_path = "".join(c for c in album if c not in special_characters) 
        author_path = "".join(c for c in yt.author if c not in special_characters)
        outpath = str(path) + "\\" + author_path + "\\" +  album_path
        yt.streams.get_by_itag(251).download(output_path=outpath)
    print("----------------------------------------------------------------------------------")
    print("    Encoding *.webm files to .flac with max. compression.")
    print("    ")
    print("----------------------------------------------------------------------------------")
    threads = list()
    for file_path in os.listdir(outpath):
        if os.path.isfile(os.path.join(outpath, file_path)) and file_path.endswith("webm"):
            subpr = "ffmpeg -i \"" + outpath + "\\" + file_path + "\" -f flac -sample_fmt s16 -ar 48000 -compression_level 12 -loglevel quiet \"" + outpath + "\\" + file_path.replace(".webm", ".flac") +"\""
            thread = threading.Thread(target=encode, args=(subpr, file_path, outpath + "\\" + file_path, ))
            threads.append(thread)
            thread.start()
    for x in threads:
        x.join()
    print("Encoding done.")
    #xrecodeargs = str(path)+"\\xrecode\\xrecode3cx64.exe " +"-i \"" + outpath + "\\*.webm\" /r -o \"" + outpath + "\" /dest flac /compression 8 /delete"
    #subprocess.call(xrecodeargs)

    print("----------------------------------------------------------------------------------")
    print("    Getting MusicBrainz album information.")
    print("    ")
    print("----------------------------------------------------------------------------------")
    mbz.set_useragent('test', '0.1')
    artist_list = mbz.search_artists(query=artist)['artist-list']
    art = artist_list[0] 
    print("Selected artist id " + art['id'] + " from MB")
    release_list = mbz.get_artist_by_id(art['id'],includes=["release-groups"], release_type=["album", "ep"])
    release_id = ""
    album_meta = ""
    getHighest = 0.0
    for release_group in release_list["artist"]["release-group-list"]:
        if similar(''.join(e for e in release_group['title'] if e.isalnum()), ''.join(e for e in album if e.isalnum())) > 0.6 and float(similar(''.join(e for e in release_group['title'] if e.isalnum()), ''.join(e for e in album if e.isalnum()))) > getHighest:
            getHighest = float(similar(''.join(e for e in release_group['title'] if e.isalnum()), ''.join(e for e in album if e.isalnum())))
            print("Album match found for " + str(similar(''.join(e for e in release_group['title'] if e.isalnum()), ''.join(e for e in album if e.isalnum())) * 100) +"%")
            album_meta = release_group['title']
            release_id = release_group['id']
    if album_meta == "":
        sys.exit("no Album found")
    if release_id != "":
        release_list = mbz.browse_releases(release_group=release_id)
        for rele in release_list['release-list']:
            medium = mbz.get_release_by_id(rele['id'],includes=["media", "recordings"])
            if medium["release"]["medium-list"][0]["track-count"] == counter and medium["release"]["medium-list"][0]['format'] == "CD" or medium["release"]["medium-list"][0]['format'] == "Digital Media":
                date_meta = medium['release']['date']
                medium = medium["release"]["medium-list"][0]["track-list"]
                break
    artist_meta = art['name']
    genre_meta = art['tag-list'][0]['name']

    print("Metadata selected for album information :")
    print("Artist: " + artist_meta)
    print("Album: " + album_meta)
    print("Release date: " + date_meta)
    print("Genre: " + genre_meta)

    print("----------------------------------------------------------------------------------")
    print("    Setting meta tags.")
    print("    ")
    print("----------------------------------------------------------------------------------")
    files =[]
    for file_path in os.listdir(outpath):
        if os.path.isfile(os.path.join(outpath, file_path)):
            if file_path.split(sep=".")[1] == "flac":
                files.append(file_path)
    for track in medium:
        print(track['position'] + ". " + track['recording']['title'])
        for file in files:
            if similar(file.split(sep=".")[0], track['recording']['title']) > 0.8:
                print("     Matching file found " + str(similar(file.split(sep=".")[0], track['recording']['title'])*100) + "%")
                audio = FLAC(outpath + "\\" + file)
                audio['title'] = track['recording']['title']
                audio['artist'] = artist_meta
                audio['album'] = album_meta
                audio['genre'] = genre_meta
                audio['year'] = date_meta.split("-")[0]
                audio['Tracknumber'] = track['position']
                audio.save()
    print("----------------------------------------------------------------------------------")
    print("    Done.")
    print("    ")
    print("##################################################################################")