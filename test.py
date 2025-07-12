from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv()
# Replace with your actual values
STORAGE_ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
FOLDER_PATH = "testt"
sas_token = os.getenv("SAS_TOKEN")

# Construct the Blob Service URL
BLOB_URL = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"


blob_service_client = BlobServiceClient(account_url=BLOB_URL, credential=sas_token)


# Get container client
container_client = blob_service_client.get_container_client(container=CONTAINER_NAME)

# List blobs in the specified folder prefix
print(f"Files in folder '{FOLDER_PATH}':")
blob_list = container_client.list_blobs(name_starts_with=FOLDER_PATH)
for blob in blob_list:
    print(blob.name)
