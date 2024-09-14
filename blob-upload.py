import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import time
from azure.core.exceptions import HttpResponseError


# Define your storage account connection string
connection_string = os.getenv('BLOB_CONNECTION_STRING')

# Define the container name
container_name = "help-docs"

# Define local directory containing files to upload
local_directory = "./local-index"

# Define the base URL you want to associate with each blob
base_url = "https://review.learn.microsoft.com/"

def upload_files_to_blob_container(connection_string, container_name, local_directory):
    # Initialize BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Get or create the container
    container_client = blob_service_client.get_container_client(container_name)

    # # Delete the container if it exists
    # if container_client.exists():
    #     container_client.delete_container()
    #     print(f"Deleted container: {container_name}")
    # # Wait for the deletion to complete
    # while container_client.exists():
    #     print(f"Waiting for container deletion to complete...")
    #     time.sleep(1)

    # Recreate the container
    # container_client.create_container()
    # print(f"Recreated container: {container_name}")

    # Upload files from the local directory to the container
    for root, _, files in os.walk(local_directory):
        for file in files:
            local_file_path = os.path.join(root, file)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file)
            blob_url = get_blob_url(file)
            with open(local_file_path, "rb") as data:
                try:
                    blob_client.upload_blob(data)
                    print(f"Uploaded '{local_file_path}' to container '{container_name}' as '{file}'")
                    # If it's a regular docs file with a URL:
                    if file.startswith("help-content") and file.endswith(".md") and "include" not in file:
                        blob_client.set_blob_metadata(metadata={"URL": blob_url})
                        print(f"Set URL metadata for blob: '{blob_url}'")
                except Exception as e:
                    print(f"An error occurred: {e}")
                    continue



def get_blob_url(filename):

    # Get the URL of the blob
    # You need to remove the .md
    new_filename = filename[:-3] if filename.endswith(".md") else filename
    # and replace all . with /
    new_filename = new_filename.replace(".", "/")
    # and replace help-content/ with help/
    new_filename = new_filename.replace("help-content/", "help/")
    blob_url = f"{base_url}{new_filename}"
    return blob_url


# Upload files to Azure Blob Storage container
upload_files_to_blob_container(connection_string, container_name, local_directory)
