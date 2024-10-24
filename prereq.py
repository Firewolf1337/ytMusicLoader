import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pytubefix"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "musicbrainzngs"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "ytmusicapi"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "flask"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "flask_socketio"])
