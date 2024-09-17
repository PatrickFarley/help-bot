from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

# Define your storage account connection string
connection_string = os.getenv('BLOB_CONNECTION_STRING')

# Define the container name
container_name = "help-docs"

# Define the base URL you want to associate with each blob
base_url = "https://review.learn.microsoft.com/"

# Create a BlobServiceClient using the connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get a reference to the container
container_client = blob_service_client.get_container_client(container_name)

# List all blobs in the container
blobs = container_client.list_blobs()

# Iterate over each blob
for blob in blobs:

    # 
    if "includes." in blob.name:
        blob_url = ""
    
        # Get a BlobClient for the current blob
        blob_client = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=blob.name)
    
        # Set metadata for the blob (including the URL)
        blob_client.set_blob_metadata(metadata={"original_url": blob_url})

        print(f"Set URL metadata for blob '{blob.name}': {blob_url}")
