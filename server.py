from flask import Flask, render_template, request
from flask_socketio import SocketIO

import subprocess
import threading

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def run_search(search_text):
    command = ["py", "searchPlaylist.py", "-w", "w", "-a", search_text]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    for line in process.stdout:
        socketio.emit('output', line.strip())
    
    process.wait()

def run_download():
    command = ["py", "download.py"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    for line in process.stdout:
        socketio.emit('output', line.strip())
    
    process.wait()

def run_single(playlist, format):
    command = ["py", "download.py", "-l", playlist, "-f", format]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        socketio.emit('output', line.strip())
    process.wait()

@socketio.on('run_search')
def handle_run_search(data):
    search_text = data['search_text']
    threading.Thread(target=run_search, args=(search_text,)).start()

@socketio.on('run_download')
def handle_run_download():
    threading.Thread(target=run_download).start()

@socketio.on('run_single')
def handle_run_single(data):
    playlist = data['playlist']
    format = data['format']
    threading.Thread(target=run_single, args=(playlist,format,)).start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
