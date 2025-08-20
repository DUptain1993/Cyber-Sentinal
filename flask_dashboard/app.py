from flask import Flask, request, redirect, url_for, send_from_directory, render_template, flash
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.getenv('SECRET_KEY')  # Load secret key from .env file

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully uploaded', 'success')
        return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(debug=True)
