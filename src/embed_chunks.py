import json

from parser import parse_pdf
from chunker import chunk_document
from embeddings import create_embedding


# --------------------------------------------------
# 1. Parse PDF
# --------------------------------------------------

pages = parse_pdf(
    "data/demopdf.pdf"
)

print(
    f"Total pages: {len(pages)}"
)


# --------------------------------------------------
# 2. Create final chunks
# --------------------------------------------------

chunks = chunk_document(
    pages,
    method="section"
)

print(
    f"Total chunks: {len(chunks)}"
)


# --------------------------------------------------
# 3. Create embeddings
# --------------------------------------------------

embedded_chunks = []

for i, chunk in enumerate(chunks):

    print(
        f"Creating embedding "
        f"{i + 1}/{len(chunks)}..."
    )

    embedding = create_embedding(
        chunk["text"]
    )

    embedded_chunks.append({

        "id": chunk["id"],

        "text": chunk["text"],

        "page_number":
            chunk["page_number"],

        "chunk_index":
            chunk["chunk_index"],

        "chunking_method":
            chunk["chunking_method"],

        "section":
            chunk["section"],

        "embedding":
            embedding
    })


# --------------------------------------------------
# 4. Save embeddings
# --------------------------------------------------

with open(
    "data/embedded_chunks.json",
    "w"
) as file:

    json.dump(
        embedded_chunks,
        file
    )


print(
    "\nEmbeddings created and saved!"
)