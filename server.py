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
    command = ["python", "searchPlaylist.py", "-w", "w", "-a", search_text]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    for line in process.stdout:
        socketio.emit('output', line.strip())
    
    process.wait()

def run_download():
    command = ["python", "download.py"]
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

if __name__ == '__main__':
    socketio.run(app, debug=True)
