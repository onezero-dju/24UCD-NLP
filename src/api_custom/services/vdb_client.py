from qdrant_client import QdrantClient
from dotenv import load_dotenv
from os import environ

load_dotenv(dotenv_path='../')  # load the `.env` file
key = environ.get('QDRANT_API_KEY')

qdrant_client = QdrantClient(
    url="https://548209f7-7e4a-4175-8d91-cb72fa1b0b68.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key=key,
)

print(qdrant_client.get_collections())