from flask import Flask, flash, request, redirect, url_for, render_template
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'mp4'}
import os
# from flask_socketio import SocketIO
# from flask_socketio import send, emit
import cv2 
import random
import vector_search as vsearch
import langchain_search as lc

app = Flask(__name__)
app.config['SECRET_fKEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

UPLOAD_FOLDER = "data"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__':
    socketio.run(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def start():
    return redirect(url_for('index'))  
    # return render_template('index.html', name="bob the bear")

@app.route('/gpt_query', methods=['GET', 'POST'])
def gpt_query():
    if request.method == 'POST':
        # check if the post request has the file part
        gptquery = request.form['gptquery']
        #function to pass query to database    
        results = vsearch.vector_search(gptquery)[0]
        video_path = "data/"+ results[2]
        print(video_path)
        detail_path = "data/"+ results[3]
        print(detail_path)
        lc.search_from(detail_path,gpt_query)
        return redirect(url_for('index'))
  
    return render_template('gpt.html')



@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        if 'details' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        #here it is 
        details = request.files['details']
        
        desc = request.form['desc']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected vidoe file')
            return redirect(request.url)
        
        if details.filename == '':
            flash('No selected details file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename) and file.filename.endswith('.mp4'):
            filename = secure_filename(file.filename)
            detailname = secure_filename(details.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], detailname))
            # test
            vsearch.insert_data(filename, desc, detailname)
            return redirect(url_for('index'))


    return render_template('upload.html')

# @socketio.on('connect')
# def test_connect():
#     emit('my response', {'data': 'Connected'})

@app.route('/redplant', methods=['GET', 'POST'])
def redplant():
    if request.method == 'POST':
        if 'buttonback' in request.form:
            return redirect(url_for('index'))
    return render_template('redplant.html')

@app.route('/pool', methods=['GET', 'POST'])
def pool():
    if request.method == 'POST':
        if 'buttonback' in request.form:
            return redirect(url_for('index'))
    return render_template('pool.html')

@app.route('/intersystems', methods=['GET', 'POST'])
def intersystems():
    if request.method == 'POST':
        if 'buttonback' in request.form:
            return redirect(url_for('index'))
    return render_template('intersystems.html')



@app.route('/index', methods=['GET', 'POST'])  # Include GET and POST methods
def index():
    if request.method == 'POST':
        if 'button1' in request.form:
            return redirect(url_for('redplant'))
        elif 'button2' in request.form:
            return redirect(url_for('pool'))  # Change to another route if needed
        elif 'button3' in request.form:
            return redirect(url_for('redplant'))  # Change to another route if needed
        elif 'upload' in request.form:
            return redirect(url_for('upload_file'))  # Change to another route if needed
        elif 'chat' in request.form:
            return redirect(url_for('gpt_query'))  # Change to another route if needed
    return render_template('index.html', name='Timothy Beaver')