import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "pytube"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "musicbrainzngs"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "mutagen"])

