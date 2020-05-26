#Main module

"""This is the main module of program where other function modules are called accordingly."""

#Importing other modules accordingly
from labler import extract_data, label_data
import subprocess
import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from utilities import *
ALLOWED_EXTENSIONS = set(['log'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file has been selected.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded. Please wait.')
            print ("\n\n=-=-=-=-=-=-=- Welcome to the HTTP anomaly detection software -=-=-=-=-=-\n")
          
            while True:
                file=input("Please specify the name of the file \nFormat [./Directory/filename] \n")
                if not file:
                    continue
                try:
                    extracted_data = extract_data(open(file, 'r'))
                except Exception as e:
                    print("An Error has occured. Please make sure the file type is correct. \nException:", str(e))
                    flash('Sorry. An error has occured', str(e))
                    return redirect(request.url)

                csv_filename = 'labeled-data-samples\\' + file.split(".")[0].split("\\")[-1] + '.csv'

                try:
                    csv_file = open(csv_filename, 'w')
                    file_path = os.path.realpath(csv_file.name)
                except Exception as e:
                    print("An Error has occured. \nException:", str(e))
                    continue

                label_data(extracted_data, csv_file)

                print("*******Feeding the file to decision tree classifier*******")
                result = subprocess.call(['python', 'decision_tree_classifier.py', '-t', './labeled-data-samples/all.csv', '-v', file_path])
                print("*******Feeding the file to logistic regression classifier*******")
                result = subprocess.call(['python', 'logistic_regression_classifier.py', '-t', './labeled-data-samples/all.csv', '-v', file_path])
                print("Thank you. The program will now terminate. \nSee you on the front end")
                break

            return redirect('/')
            
            return redirect(request.url)
        else:
            flash('Only .log files are accepted')
            return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)








   
