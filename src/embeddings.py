import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


def create_embedding(text: str):

    response = client.embeddings.create(
        model="openai/text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


if __name__ == "__main__":

    text = """
    Binary search is an efficient algorithm used
    to search for an element in a sorted array.
    """

    embedding = create_embedding(text)

    print("\nTEXT:")
    print(text.strip())

    print("\nVECTOR DIMENSION:")
    print(len(embedding))

    print("\nFIRST 10 VECTOR VALUES:")
    print(embedding[:10])