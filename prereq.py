import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "pytubefix"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "musicbrainzngs"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "ytmusicapi"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "flask_socketio"])
