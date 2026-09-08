import os

from dotenv import load_dotenv
from pinecone import Pinecone


load_dotenv(".env")


pinecone_api_key = os.getenv("PINECONE_API_KEY")


pc = Pinecone(
    api_key=pinecone_api_key
)


index = pc.Index("sde-rag-lab")


if __name__ == "__main__":

    stats = index.describe_index_stats()

    print(stats)