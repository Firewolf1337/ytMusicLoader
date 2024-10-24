from pytubefix import YouTube,Playlist
import pathlib
import sys
import subprocess
import musicbrainzngs as mbz 
from difflib import SequenceMatcher
import os
import threading
import argparse
from typing import Dict

parser = argparse.ArgumentParser()
parser.add_argument('--links', '-l', help="Playlist links. Can be whitespace separated", type= str)
parser.add_argument('--format', '-f', help="Output format. Possible arguments none, mp3 or flac", type= str, default= "mp3", choices=['flac', 'mp3', 'none'])
args = parser.parse_args()

# If proxy is used uncomment this
#proxy = 'http://1.2.3.4:8080'
#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy


path = pathlib.Path(__file__).parent.resolve()
urls = []
fileext = ""
outformat= ""
if args.links:
    urls = args.links.split(" ")
else:
    with open(os.path.join(path, "playlists.txt"), "r") as Playlists:
        urls = Playlists.readlines()


if os.name == 'nt':
    ffmpegpath = "\"" + str(os.path.join(path, 'ffmpeg','bin','ffmpeg.exe')) + "\" "
    print("OS Windows")
    if os.getenv('PATH').__contains__('ffmpeg'):
        ffmpegpath = "ffmpeg "
else:
    if subprocess.getstatusoutput('ffmpeg')[0] == 1:
        ffmpegpath = "ffmpeg "

def add_metadata(file: pathlib.Path,
                 meta: Dict[str, str],
                 save_path: pathlib.Path = None,
                 overwrite: bool = True):
    if not save_path:
        save_path = file.with_suffix('.metadata' + file.suffix)

    metadata_args = ""
    for k, v in meta.items():
        metadata_args = metadata_args + " -metadata " + f"\"{k}={v}\""

    args = ffmpegpath + "-v quiet -i \"" + str(file.absolute()) + "\"" + metadata_args + " -c copy \"" + str(save_path) + "\""
    if overwrite:
        args = args + " -y"
    proc = subprocess.run(args, stdout=subprocess.PIPE, shell=True)
    proc.check_returncode()
    os.remove(file)

def switch(format):
    global fileext
    global outformat
    if format == "mp3":
        fileext = ".mp3"
        outformat =  "-f mp3 -ac 2 -b:a 320k -loglevel quiet"
    elif format == "flac":
        fileext = ".flac"
        outformat =  "-f flac -sample_fmt s16 -ar 48000 -compression_level 12 -loglevel quiet"
    elif format == "none":
        fileext = ".webm"
        outformat = "none"

switch(args.format)

special_characters=['<','>',':','|','&','(',')','*','\\','/', '?', '\"']
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def encode(param, name, inputfile):
    print("Start encoding ", name, flush=True)
    subprocess.call(param, shell=True)
    os.remove(inputfile)

for url in urls:
    if not url:
        continue 
    p = Playlist(url=url)
    album = (p.title).replace('Album - ', '')
    artist = (p.videos[0]).author
    album_path = "".join(c for c in album if c not in special_characters) 
    author_path = "".join(c for c in artist if c not in special_characters)
    outpath = os.path.join(path, 'downloads', author_path, album_path)
    pathlib.Path(outpath).mkdir(parents=True, exist_ok=True)
    print("##################################################################################", flush=True)
    print("    Downloading " + album + " from " + artist, flush=True)
    print("    to \"" +  str(outpath) + "\"", flush=True)
    print("----------------------------------------------------------------------------------", flush=True)
    counter = 0
    for yt in p.videos:
        counter = counter + 1
        print("Loading \"" + str(yt.title) + "\" " + str(counter) + "/" + str(p.length), flush=True)
        try:
            yt.streams.get_by_itag(251).download(output_path=outpath)
        except:
            print("Something wrong with the stream of track " + str(yt.title))
    if counter < p.length:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", flush=True)
        print("    Processing stopped for " + album + " from " + artist, flush=True)
        print("    The album does not seem to be complete!", flush=True)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", flush=True)
        continue
    if outformat != "none":
        print("----------------------------------------------------------------------------------", flush=True)
        print("    Encoding *.webm files to " + args.format + ".", flush=True)
        print("    ", flush=True)
        print("----------------------------------------------------------------------------------", flush=True)

        threads = list()
        for file_path in os.listdir(outpath):
            if os.path.isfile(os.path.join(outpath, file_path)) and file_path.endswith("webm"):
                fpath = os.path.join(outpath, file_path)
                subpr = str(ffmpegpath) +  "-i \"" + fpath + "\" "+ outformat + " \"" + fpath .replace(".webm", fileext) +"\""
                thread = threading.Thread(target=encode, args=(subpr, file_path, fpath, ))
                threads.append(thread)
                thread.start()
        for x in threads:
            x.join()
        print("Encoding done.", flush=True)

    print("----------------------------------------------------------------------------------", flush=True)
    print("    Getting MusicBrainz album information.", flush=True)
    print("    ", flush=True)
    print("----------------------------------------------------------------------------------", flush=True)
    mbz.set_useragent('test', '0.1')
    artist_list = mbz.search_artists(query=artist)['artist-list']
    art = artist_list[0] 
    print("Selected artist id " + art['id'] + " from MB", flush=True)
    release_list = mbz.get_artist_by_id(art['id'],includes=["release-groups"], release_type=["album", "ep"])
    release_id = ""
    album_meta = ""
    getHighest = 0.0
    for release_group in release_list["artist"]["release-group-list"]:
        if similar(''.join(e for e in release_group['title'] if e.isalnum()), ''.join(e for e in album if e.isalnum())) > 0.6 and float(similar(''.join(e for e in release_group['title'] if e.isalnum()), ''.join(e for e in album if e.isalnum()))) > getHighest:
            getHighest = float(similar(''.join(e for e in release_group['title'] if e.isalnum()), ''.join(e for e in album if e.isalnum())))
            print("Album match found for " + str(similar(''.join(e for e in release_group['title'] if e.isalnum()), ''.join(e for e in album if e.isalnum())) * 100) +"%", flush=True)
            album_meta = release_group['title']
            release_id = release_group['id']
    if album_meta == "":
        print("no Album found. Skipping to next Download. Files will remain on disk.", flush=True)
        continue
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

    print("Metadata selected for album information :", flush=True)
    print("Artist: " + artist_meta, flush=True)
    print("Album: " + album_meta, flush=True)
    print("Release date: " + date_meta, flush=True)
    print("Genre: " + genre_meta, flush=True)

    print("----------------------------------------------------------------------------------", flush=True)
    print("    Setting meta tags.", flush=True)
    print("    ", flush=True)
    print("----------------------------------------------------------------------------------", flush=True)
    files =[]
    for file_path in os.listdir(outpath):
        if os.path.isfile(os.path.join(outpath, file_path)):
            if file_path.split(sep=".")[1] == fileext.replace(".",""):
                files.append(file_path)
    for track in medium:
        print(track['position'] + ". " + track['recording']['title'], flush=True)
        title_path = "".join(c for c in track['recording']['title'] if c not in special_characters)
        for file in files:
            if similar(file.split(sep=".")[0], track['recording']['title']) > 0.8:
                print("     Matching file found " + str(similar(file.split(sep=".")[0], track['recording']['title'])*100) + "%", flush=True)
                fpath = os.path.join(outpath, file)
                f = pathlib.Path(fpath)
                add_metadata(
                    f,
                    meta=dict(
                        title=track['recording']['title'],
                        artist=artist_meta,
                        album=album_meta,
                        genre=genre_meta,
                        year=date_meta.split("-")[0],
                        date=date_meta.split("-")[0],
                        track=track['position'],
                        Tracknumber=track['position'],
                    ),
                    overwrite=True,
                    save_path=os.path.join(outpath, track['position'] + " - " + artist_meta  + " - " + album_meta + " - " + title_path + f.suffix)
                )                    
    print("----------------------------------------------------------------------------------", flush=True)
    print("    Done.", flush=True)
    print("    ", flush=True)
    print("##################################################################################", flush=True)
