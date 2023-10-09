from flask import Flask, request, render_template_string, Markup
import subprocess
import multiprocessing

app = Flask(__name__)

# Global variable to store the subprocess
subprocess_handler = None
subpr = None

# Define the download_script function separately
def download_script():
    global subpr
    try:
        subpr = subprocess.Popen(['python', 'download.py', '-f', 'mp3'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(subpr.pid)
        return subpr
    except Exception as e:
        return None

form_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>String to Python</title>
</head>
<body>
    <form method="POST" action="/artist">
        <input type="text" name="text" placeholder="Artist name">
        <input type="submit" value="Fetch Playlists">
    </form>
    <form method="POST" action="/download">
        <input type="submit" name="btn" value="Download">
    </form>
    <div>{{ response | safe }}</div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(form_html, response="")

@app.route('/artist', methods=['POST'])
def received_string():
    received_text = request.form.get('text', '')
    result = subprocess.run(['python', 'searchPlaylist.py', '-w', 'a', '-a', received_text], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode == 0:
        ausgabezeilen = result.stdout.strip().split('\n')
        response = Markup('<br>'.join(ausgabezeilen))
    else:
        response = f'Error searching for Playlists: {result.stderr}'
    
    return render_template_string(form_html, response=response)

@app.route('/download', methods=['POST'])
def run_download():
    global subprocess_handler
    result = None
    
    if not subprocess_handler or not subprocess_handler.is_alive():
        subprocess_handler = multiprocessing.Process(target=download_script)
        subprocess_handler.daemon = True
        subprocess_handler.start()
    
    subprocess_handler.join(timeout=0.1)  # Check for subprocess completion without blocking
    
    if subprocess_handler.is_alive():
        response = 'Download in progress...'
    else:
        result = subprocess_handler.exitcode
        if result == 0:
            returnstring = subprocess_handler.stdout.strip().split('\n')
            response = Markup('<br>'.join(returnstring))
        else:
            response = f'Error running download.py: {subprocess_handler.stderr}' if result else 'Error running download.py.'
    
    return render_template_string(form_html, response=response)

@app.route('/cancel', methods=['POST'])
def cancel_download():
    global subprocess_handler
    global subpr

    if subpr and subpr.poll() is None:
        try:
            subpr.terminate()
        except Exception as e:
            return f'Error cancelling download: {str(e)}'

    if subprocess_handler and subprocess_handler.is_alive():
        try:
            subprocess_handler.terminate()
        except Exception as e:
            return f'Error cancelling download: {str(e)}'

        response = 'Download cancelled.'
    else:
        response = 'No active download to cancel.'

    return render_template_string(form_html, response=response)

if __name__ == '__main__':
    app.run(debug=True)