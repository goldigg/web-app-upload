import json
from flask import Flask, request, redirect, render_template, session, url_for
from werkzeug.utils import secure_filename
from presigned_url import *
import boto3
from botocore.config import Config
import os




app = Flask(__name__)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)


s3BucketName = "ggoldmann-pgs-upskill"
config = Config(
    region_name = 'eu-central-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)


@app.route("/upload", methods=["POST"])
def upload_file():
    print(f"Upload started")
    s3_client = boto3.client('s3', config=config)
    if "file" not in request.files:
        return "No file key in request.files"
    print(f'File {request.files["file"]} ')
    file = request.files["file"]
    
    if file.filename == "":
        return "Please select a file"
    print(f'S3 client {s3_client} ')
    file.filename = secure_filename(file.filename)    
    presigned_s3= generate_presigned_url(s3_client, {'Bucket': s3BucketName, 'Key': file.filename }, 60)

    print ("presigned_s3:", presigned_s3)

    content = file.read()
    messages=""
    try:
        response = requests.post(presigned_s3['url'], data=presigned_s3['fields'], files= {'file': content } )
        messages=(f"Uploaded to bucket {response.status_code}")
        print(f'Msg: {messages}')
    except FileNotFoundError:
        print(f"Couldn't find {file.filename}. For a PUT operation, the key must be the "
              f"name of a file that exists on your computer.")
    else:
        return redirect(url_for('s3_form'))

@app.route("/s3", methods=["GET"])
def s3_form(messages=""):
    data = requests.get(os.environ['WEB_ENDPOINT'])
    data = json.loads(data.content)
    host = request.host
    print(f"Msg: {messages}")
    return render_template('s3_form.html', data=data, host=host, info=messages)

@app.route("/health", methods=["GET"])
def health():
    return "200"
