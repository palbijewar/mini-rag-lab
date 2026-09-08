import os
from dotenv import load_dotenv
from openai import OpenAI
import math

load_dotenv(".env")

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key
)


def create_embedding(text: str):

    response = client.embeddings.create(
        model="openai/text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def cosine_similarity(vector_a, vector_b):

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    return dot_product / (
        magnitude_a * magnitude_b
    )


if __name__ == "__main__":

    text_1 = "How does binary search work?"

    text_2 = "Explain the algorithm used to search a sorted array."

    text_3 = "How do I cook chicken curry?"


    embedding_1 = create_embedding(text_1)

    embedding_2 = create_embedding(text_2)

    embedding_3 = create_embedding(text_3)


    similarity_1_2 = cosine_similarity(
        embedding_1,
        embedding_2
    )

    similarity_1_3 = cosine_similarity(
        embedding_1,
        embedding_3
    )


    print("\nTEXT 1:")
    print(text_1)

    print("\nTEXT 2:")
    print(text_2)

    print("\nTEXT 3:")
    print(text_3)


    print("\nSIMILARITY BETWEEN TEXT 1 AND TEXT 2:")
    print(similarity_1_2)

    print("\nSIMILARITY BETWEEN TEXT 1 AND TEXT 3:")
    print(similarity_1_3)