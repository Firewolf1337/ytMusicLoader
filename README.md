# ytMusicLoader
## Python Downloader for  Youtube Music:
### Installation:
1. Install Python 3
1. Install pip - ```py -m ensurepip --upgrade```
1. Install prerequisites - ```python .\prereq.py```
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
```

### Run a download:
Either run - ```python .\download.py https://music.youtube.com/playlist?list=XXXXXX```  
or put the link in the playlists.txt and just run ```python .\download.py```  
**_For multiple link downloads put the links behind ```.\download.py``` seperated by a whitespace or put every link in a new line in the playlists.txt._**  

### Note:
Just tested with music.youtube.com and urls with ```...playlist?list=....```

## Thanks going to:
**To all contributers at:**
* [pytube](https://github.com/pytube/pytube)
* [musicbrainzngs](https://github.com/alastair/python-musicbrainzngs)
* [mutagen](https://github.com/quodlibet/mutagen)
* [FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases)
