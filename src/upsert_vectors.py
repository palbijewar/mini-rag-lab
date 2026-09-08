import json

from pinecone_client import index


# -----------------------------
# Load embedded chunks
# -----------------------------

with open(
    "data/embedded_chunks.json",
    "r",
    encoding="utf-8"
) as file:

    chunks = json.load(file)


print(f"Loaded {len(chunks)} chunks")


# -----------------------------
# Prepare Pinecone records
# -----------------------------

vectors = []

for chunk in chunks:

    vector = {
        "id": chunk["id"],

        "values": chunk["embedding"],

        "metadata": {
            "text": chunk["text"],
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
            "chunking_method": chunk["chunking_method"]
        }
    }

    vectors.append(vector)


print(f"Prepared {len(vectors)} vectors")


# -----------------------------
# Upload to Pinecone
# -----------------------------

index.upsert(
    vectors=vectors
)


print("Vectors uploaded successfully!")