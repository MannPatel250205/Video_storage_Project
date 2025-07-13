from flask import Flask, request, jsonify, render_template, flash, redirect
from azure.storage.blob import BlobServiceClient, ContentSettings
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')

ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
SAS_TOKEN = os.getenv("SAS_TOKEN")
BLOB_URL = f"https://{ACCOUNT_NAME}.blob.core.windows.net"
blob_service_client = BlobServiceClient(account_url=BLOB_URL, credential=SAS_TOKEN)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)


def check_password(password):
    return password == os.getenv('PASSWORD')



@app.route('/api/list', methods=['GET'])
def list_folder():
    prefix = request.args.get('path', '').strip('/')
    
    if prefix and not prefix.endswith('/'):
        prefix += '/'
    

    seen_dirs = set()
    files = []
    for blob in container_client.list_blobs(name_starts_with=prefix):
        path_parts = blob.name[len(prefix):].split('/')
        if len(path_parts) == 1:
            if blob.name.endswith('/.keep'):  # folder marker
                continue
            files.append({
                "name": path_parts[0],
                "type": "file",
                "url": generate_blob_sas_url(blob.name)
            })
        else:
            folder_name = path_parts[0]
            if folder_name not in seen_dirs:
                seen_dirs.add(folder_name)
                files.append({
                    "name": folder_name,
                    "type": "folder"
                })

    return jsonify(files)


@app.route('/api/delete', methods=['POST'])
def delete_file():
    blob_name = request.json.get('blob_name')
    if not blob_name:
        return jsonify({"error": "Missing blob_name"}), 400
    try:
        container_client.delete_blob(blob_name)
        return jsonify({"message": "File deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/create-folder', methods=['POST'])
def create_folder():
    folder_path = request.json.get('path', '').strip('/')
    if not folder_path:
        return jsonify({'error': 'Path is required'}), 400
    blob_name = f"{folder_path}/.keep"
    try:
        container_client.upload_blob(blob_name, b'', overwrite=True)
        return jsonify({'message': 'Folder created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/api/list-files', methods=['GET'])
# def list_files():
#     prefix = request.args.get('directory', '')
#     blobs = container_client.list_blobs(name_starts_with=prefix)
#     file_list = [
#         {
#             "name": blob.name,
#             "url": generate_blob_sas_url(blob.name)
#         }
#         for blob in blobs if not blob.name.endswith('/')
#     ]

#     return jsonify(file_list)


@app.route('/api/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    path = request.form.get('path', '').strip('/')
    if file and file.filename:
        blob_name = f"{path}/{file.filename}" if path else file.filename
        try:
            container_client.upload_blob(
                name=blob_name,
                data=file,
                overwrite=True,
                content_settings=ContentSettings(content_type=file.content_type)
            )
            return jsonify({"message": "Upload successful", "blob_name": blob_name}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No file provided"}), 400


# @app.route('/api/generate-url', methods=['GET'])
# def generate_url():
#     blob_name = request.args.get('blob_name')
#     if not blob_name:
#         return jsonify({"error": "Missing blob_name"}), 400
#     return jsonify({"url": generate_blob_sas_url(blob_name)})


def generate_blob_sas_url(blob_name):

    return f"{BLOB_URL}/{CONTAINER_NAME}/{blob_name}?{SAS_TOKEN}"


@app.route('/')
def index():
    return "React frontend served separately."


if __name__ == '__main__':
    app.run(debug=True)