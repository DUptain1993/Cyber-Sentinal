from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key-for-development')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

# Export the Flask app for Vercel
app.debug = False
