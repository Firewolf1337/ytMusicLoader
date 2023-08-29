﻿# ytMusicLoader
## Python Downloader for  Youtube Music:
### Installation:
1. Install Python 3
1. Install pip - ```py -m ensurepip --upgrade```
1. Install prerequisites - ```python .\prereq.py```
1. Download xrecode3 command line version and extract in a xrecode folder beside the python files.

### Folderstructure shoul look like this:
```
ytMusicLoader/
├── xrecode/
│   ├── bin/
|   |    ├── ...
│   ├── portable/
|   |    ├── ...
│   ├── stuff/
|   |    ├── ...
│   └── xrecode3cx64.exe
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
