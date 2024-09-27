from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import SearchIndex, SearchIndexerDataSourceConnection, SearchIndexerSkillset, SearchIndexer, SearchIndexerSkill
from dotenv import load_dotenv
import os
import json

load_dotenv()

endpoint = os.environ["SEARCH_ENDPOINT"]
key = os.environ["SEARCH_KEY"]
blob_connection_string = os.environ["BLOB_CONNECTION_STRING"].replace("\"","")
oai_key = os.environ["OAI_KEY"]
client = SearchIndexerClient(endpoint, AzureKeyCredential(key))
index_client = SearchIndexClient(endpoint, AzureKeyCredential(key))

def create_data_source_connection(datasource_json: dict):
    # [START create_data_source_connection]
    data_source_connection = SearchIndexerDataSourceConnection.from_dict(datasource_json)
    data_source_connection.connection_string = blob_connection_string
    return client.create_or_update_data_source_connection(data_source_connection)

def create_indexer(indexer_json: dict):
    indexer = SearchIndexer.from_dict(indexer_json)
    return client.create_or_update_indexer(indexer)
    
def create_index(index_json: dict):
    index = SearchIndex.from_dict(index_json)
    oai_vectorizer = index.vector_search.vectorizers[0].as_dict()
    oai_vectorizer["api_key"] = oai_key
    index.vector_search.vectorizers[0] = oai_vectorizer
    return index_client.create_or_update_index(index)

def create_skillset(skillset_json: dict):
    skillset = SearchIndexerSkillset.from_dict(skillset_json)
    # set key to oai resource
    oai_skill = skillset.skills[1].as_dict()
    oai_skill["api_key"] = oai_key
    skillset.skills[1] = SearchIndexerSkill.from_dict(oai_skill)
    return client.create_or_update_skillset(skillset)


deploy_ops = [
    ("datasource.json",create_data_source_connection),
    ("index.json",create_index),
    ("skillset.json",create_skillset),
    ("indexer.json",create_indexer),
]
def deploy_all(index_root: str):
    index_artifacts = os.listdir(index_root)
    for dirent in index_artifacts:
        if os.path.isdir(f"{index_root}/{dirent}"):
            print(f"deploying: {dirent}")
            for filename, deploy_func in deploy_ops:
                if filename in os.listdir(f"{index_root}/{dirent}"):
                    artifact_json = json.load(open(f"{index_root}/{dirent}/{filename}","r"))
                    deploy_func(artifact_json)

                





deploy_all("indexes")




