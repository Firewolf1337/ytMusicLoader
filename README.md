# ytMusicLoader
## Python Downloader for  Youtube Music:
### Installation:
1. Install Python 3
1. Install pip - ```py -m ensurepip --upgrade```
1. Install prerequisites - ```py .\prereq.py```
1. Download [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases) and extract atleast the bin folder to a ffmpeg folder where the python files are.

### Folder structure should atleast look like this:
```
ytMusicLoader/
├── ffmpeg/
│   ├── bin/
|   |    ├── ffmpeg.exe
│   └── ...
├── download.py
├── playlists.txt
└── prereq.py
└── searchPlaylist.py
```


### Run a download:
Either run - ```py .\download.py -l https://music.youtube.com/playlist?list=XXXXXX -f mp3```  
or put the link in the playlists.txt and just run ```py .\download.py```  
**_For multiple link downloads put the links behind```.\download.py -l``` seperated by a whitespace and surroundet by quotes or put every link in a new line in the playlists.txt._** 

usage: download.py [-h] [--links LINKS] [--format FORMAT]
optional arguments:
  -h, --help            show this help message and exit
  --links LINKS, -l LINKS
                        Playlist links. Can be whitespace seperated
  --format FORMAT, -f FORMAT
                        Output format. Possible arguments mp3 or flac

### Note:
Just tested with music.youtube.com and urls with ```...playlist?list=....```

### Search for playlists:
run - ```py .\searchPlaylist.py -a "Artist Name" -w a```  
this will search for all released albums of an artist and append the list of playlists in playlists.txt

usage: searchPlaylist.py [-h] [--artist ARTIST] [--writemode {a,w}]
optional arguments:
  -h, --help            show this help message and exit
  --artist ARTIST, -a ARTIST
                        Name of the Artist to search for the albums
  --writemode {a,w}, -w {a,w}
                        Append or overwrite the existing Playlist.txt - Options a for append or w for overwrite

## Thanks going to:
**To all contributers at:**
* [pytube](https://github.com/pytube/pytube)
* [musicbrainzngs](https://github.com/alastair/python-musicbrainzngs)
* [mutagen](https://github.com/quodlibet/mutagen)
* [FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases)
