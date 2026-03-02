from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from langchain.tools import tool
from openai import OpenAI
import os

load_dotenv(".secrets")

embedding_fn = OpenAIEmbeddingFunction(
    api_key="any value",
    api_base="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    model_name="text-embedding-3-small",
    default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')}
)

vector_db_client_url="http://localhost:8000"
chroma = chromadb.HttpClient(host=vector_db_client_url)
collection = chroma.get_collection(name="career_plan", embedding_function=embedding_fn)


@tool
def career_plan(query: str, n_results: int = 1):
    """Use this tool for any questions about career plans, career development, career goals, 
    career strategies, or professional growth recommendations."""
    text = query.replace("\n", " ")
    results = collection.query(query_texts=[text], n_results=n_results)

    return results['documents'][0]