# ytMusicLoader
## Python Downloader for  Youtube Music:
### Installation:
1. Install Python 3
1. Install pip - ```py -m ensurepip --upgrade```
1. Install prerequisites - ```py .\prereq.py```
1. Download [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases) and extract at least the bin folder to a ffmpeg folder where the python files are.
1. Or just install it and make sure it is available in the cmd otherwise add it to $PATH 

### Folder structure should at least look like this:
```
ytMusicLoader/
├── ffmpeg/
│   ├── bin/
|   |    ├── ffmpeg.exe
│   └── ...
├── templates/
│   └── index.html
├── download.py
├── playlists.txt
├── prereq.py
├── searchPlaylist.py
└── server.py
```


### Run a download:
Either run - ```py .\download.py -l https://music.youtube.com/playlist?list=XXXXXX -f mp3```  
or put the link in the playlists.txt and just run ```py .\download.py```  
Format can be as is [none], mp3 or flac.

**_For multiple link downloads put the links behind```.\download.py -l``` separated by a whitespace and surrounded by quotes or put every link in a new line in the playlists.txt._** 

```
usage: download.py [-h] [--links LINKS] [--format FORMAT]
optional arguments:
  -h, --help            show this help message and exit
  --links LINKS, -l LINKS
                        Playlist links. Can be whitespace seperated
  --format FORMAT, -f FORMAT
                        Output format. Possible arguments none, mp3 or flac
```

### Note:
Just tested with music.youtube.com and urls with ```...playlist?list=....```

### Search for playlists:
run - ```py .\searchPlaylist.py -a "Artist Name" -w a```  
this will search for all released albums of an artist and append the list of playlists in playlists.txt

```
usage: searchPlaylist.py [-h] [--artist ARTIST] [--writemode {a,w}]
optional arguments:
  -h, --help            show this help message and exit
  --artist ARTIST, -a ARTIST
                        Name of the Artist to search for the albums
  --writemode {a,w}, -w {a,w}
                        Append or overwrite the existing Playlist.txt - Options a for append or w for overwrite
```

### Website interface:
run - ```py .\server.py```  
no need to handle any other commands beside this. Just run this and open the local website [http://127.0.0.1:5000](http://127.0.0.1:5000)  
Put in the name of the artist in the text field.  
Click on "Fetch Playlists". This is overwriting so only one Artist at a time is possible.  
After seeing the list of found albums, just click "Download" and relax. The script output will be shown on the website.  

## Thanks to:
**all contributers at:**
* [pytube](https://github.com/pytube/pytube)
* [musicbrainzngs](https://github.com/alastair/python-musicbrainzngs)
* [FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases)
* [ytmusicapi](https://github.com/sigma67/ytmusicapi)
* [flask](https://github.com/pallets/flask)
* [flask-socketio](https://github.com/miguelgrinberg/Flask-SocketIO)
