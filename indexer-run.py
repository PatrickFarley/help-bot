from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import SearchIndexerDataContainer
import time

def refresh_and_run_indexer(endpoint, api_key, indexer_name):
    # Create a Search Indexer Client
    credentials = AzureKeyCredential(api_key)
    indexer_client = SearchIndexerClient(endpoint=endpoint, credential=credentials)

    # Refresh the indexer
    print(f"reset Indexer: '{indexer_name}'")
    indexer_client.reset_indexer(indexer_name)

    # Run the indexer
    print(f"Running indexer: '{indexer_name}'")
    indexer_client.run_indexer(indexer_name)

    # check the indexer status and loop until it's finished:
    while True:
        # wait for 5 seconds
        time.sleep(5)
        status = indexer_client.get_indexer_status(indexer_name)
        if status.last_result.status == "inProgress":
            print("Indexer in progress...")
        elif status.last_result.status == "transientFailure":
            print("Indexer encountered an error:")
            print(status.last_result.errors)
            break
        elif status.last_result.status == "success":
            print("Indexer run successful!")
            break
        else:
            print("Unknown indexer status")



# Azure Search service endpoint
endpoint = "https://pafarley-search.search.windows.net/"
# API key for authentication
api_key = os.getenv("AZURE_SEARCH_KEY")
# Name of the indexer to refresh and run
indexer_name = "indexer-9-12"

refresh_and_run_indexer(endpoint, api_key, indexer_name)
