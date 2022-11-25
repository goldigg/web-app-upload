import json
from flask import Flask, request, redirect, render_template, session
from werkzeug.utils import secure_filename
from presigned_url import *
import boto3
from botocore.config import Config
import os




app = Flask(__name__)

config = Config(
    region_name = 'eu-central-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

s3_client = boto3.client('s3', config=config)
s3BucketName = "ggoldmann-pgs-upskill"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file key in request.files"

    file = request.files["file"]
    
    if file.filename == "":
        return "Please select a file"
    file.filename = secure_filename(file.filename)    
    presigned_s3= generate_presigned_url(s3_client, {'Bucket': s3BucketName, 'Key': file.filename }, 60)

    print ("presigned_s3:", presigned_s3)

    content = file.read()

    try:
        response = requests.post(presigned_s3['url'], data=presigned_s3['fields'], files= {'file': content } )
        session['messages']="Uploaded to bucket ${response.status_code}" 
    except FileNotFoundError:
        print(f"Couldn't find {file.filename}. For a PUT operation, the key must be the "
              f"name of a file that exists on your computer.")
    else:
        return redirect(url_for('/s3', messages=messages))

@app.route("/s3", methods=["GET"])
def s3_form():
    data = requests.get(os.environ['WEB_ENDPOINT'])
    data = json.loads(data.content)
    host = request.host
    messages = request.args['messages']  # counterpart for url_for()
    info = session['messages']       # counterpart for session
    return render_template('s3_form.html', data=data, host=host, info=info)

@app.route("/health", methods=["GET"])
def health():
    return "200"
