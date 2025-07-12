from flask import Flask, request, jsonify, render_template, flash, redirect
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
import os
from azure.storage.blob import BlobServiceClient, ContentSettings
from dotenv import load_dotenv


app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')
load_dotenv()

# Load environment variables
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
SAS_TOKEN = os.getenv("SAS_TOKEN")
BLOB_URL = f"https://{ACCOUNT_NAME}.blob.core.windows.net"
blob_service_client = BlobServiceClient(account_url=BLOB_URL, credential=SAS_TOKEN)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)





@app.route('/upload-video', methods=['POST'])
def upload_video():
    file = request.files.get('video')
    if file and file.filename:
        blob_name = f"uploads/{file.filename}"  # folder in blob container
        try:
            container_client.upload_blob(
                name=blob_name,
                data=file,
                overwrite=True,
                content_settings=ContentSettings(content_type='video/mp4')
            )
            flash(f"Video '{file.filename}' uploaded successfully to Azure Blob Storage!", "success")
        except Exception as e:
            flash(f"Failed to upload: {str(e)}", "danger")
    else:
        flash("No file selected!", "warning")
    return redirect('/')




@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
