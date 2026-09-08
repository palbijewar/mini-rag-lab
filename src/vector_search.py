from embeddings import create_embedding
from similarity import cosine_similarity


documents = [
    {
        "id": "doc-1",
        "text": "Binary search finds an element in a sorted array."
    },
    {
        "id": "doc-2",
        "text": "Hash maps store information using key-value pairs."
    },
    {
        "id": "doc-3",
        "text": "Trees organize data in a hierarchical structure."
    },
    {
        "id": "doc-4",
        "text": "Chicken curry is prepared using chicken and spices."
    },
    {
        "id": "doc-5",
        "text": "Merge sort uses the divide and conquer technique."
    }
]


# -----------------------------
# Step 1: Embed our documents
# -----------------------------

for document in documents:

    document["embedding"] = create_embedding(
        document["text"]
    )


# -----------------------------
# Step 2: Search function
# -----------------------------

def search(query: str, top_k: int = 3):

    # Convert user question into vector
    query_embedding = create_embedding(query)

    results = []

    # Compare query against every document
    for document in documents:

        score = cosine_similarity(
            query_embedding,
            document["embedding"]
        )

        results.append({
            "id": document["id"],
            "text": document["text"],
            "score": score
        })

    # Highest similarity first
    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    # Return only top K
    return results[:top_k]


if __name__ == "__main__":

    query = "How can I search efficiently in a sorted list?"

    results = search(
        query=query,
        top_k=3
    )

    print("\nQUERY:")
    print(query)

    print("\nTOP RESULTS:")

    for result in results:

        print("\n" + "=" * 60)

        print("ID:", result["id"])
        print("SCORE:", result["score"])
        print("TEXT:", result["text"])