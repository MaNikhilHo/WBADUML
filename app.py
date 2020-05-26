from flask import Flask
#importing flask module
UPLOAD_FOLDER = 'D:/FYP DEV/FYP/ok/raw-http-logs-samples'
#setting up path for the file to download
app = Flask(__name__)
app.secret_key = "secret key"
#secret key to connect
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
#max file size