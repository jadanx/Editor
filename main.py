
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import cv2
import uuid


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['STATIC_FOLDER'] = 'static'
app.static_folder = app.config['STATIC_FOLDER']
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(filename):
    unique_id = str(uuid.uuid4())[:8]
    name, extension = os.path.splitext(filename)
    return f"{name}_{unique_id}{extension}"
# Load wordlist from file
with open("wordlist/gray.txt", "r") as file:
    wordlist = set(word.strip().lower() for word in file.readlines())

def has_matching_word(sentence):
    words = set(sentence.lower().split())
    return any(any(phrase in sentence.lower() for phrase in wordlist) for word in words)
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        original_filepath = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        file.save(original_filepath)

        # Generate the filename for the grayscale image
    
        converted_filename = f"edit_{original_filename}"
        converted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], converted_filename)

        # Convert the image to grayscale using OpenCV
    matching = False
    if request.method == "POST":
       user_input = request.form.get("action", "")
       matching = has_matching_word(user_input)

  #var = 'gray'
   # if request.form['action'] == var:  
    if matching:
      img = cv2.imread(original_filepath, cv2.IMREAD_GRAYSCALE)
      cv2.imwrite(converted_filepath, img)

            # Pass filenames to the template
      return render_template('index.html', original_image=original_filename, converted_image=converted_filename)
      
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

