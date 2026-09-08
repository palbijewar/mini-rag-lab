from embeddings import create_embedding
from pinecone_client import index


def retrieve(query: str, top_k: int = 5):

    # 1. Convert user question into a vector
    query_embedding = create_embedding(query)

    # 2. Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return results


if __name__ == "__main__":

    query = "What are the most important data structures for SDE interviews?"

    results = retrieve(
        query=query,
        top_k=5
    )

    print("\nQUERY:")
    print(query)

    print("\nTOP RESULTS:")

    for i, match in enumerate(results["matches"]):

        print("\n" + "=" * 80)

        print(f"RANK: {i + 1}")
        print(f"ID: {match['id']}")
        print(f"SCORE: {match['score']}")

        metadata = match.get("metadata", {})

        print(f"PAGE: {metadata.get('page_number')}")
        print(f"CHUNK: {metadata.get('chunk_index')}")

        print("\nTEXT:")
        print(metadata.get("text"))