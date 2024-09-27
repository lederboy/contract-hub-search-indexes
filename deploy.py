from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import SearchIndexerDataContainer, SearchIndexerDataSourceConnection, SearchIndexerSkillset

from dotenv import load_dotenv
import os

load_dotenv()

endpoint = os.environ["SEARCH_ENDPOINT"]
key = os.environ["SEARCH_KEY"]
blob_connection_string = os.environ["BLOB_CONNECTION_STRING"].replace("\"","")

client = SearchIndexerClient(endpoint, AzureKeyCredential(key))

def create_data_source_connection():
    # [START create_data_source_connection]
    container = SearchIndexerDataContainer(name='contracts',query='contracts/pharmacy')
    data_source_connection = SearchIndexerDataSourceConnection(
        name="sample-data-source-connection-1",
        type="azureblob",
        connection_string=blob_connection_string,
        container=container,
        
    )
    result = client.create_data_source_connection(data_source_connection)

create_data_source_connection()