import json

from parser import parse_pdf
from chunker import chunk_document
from embeddings import create_embedding


if __name__ == "__main__":

    pages = parse_pdf("data/demopdf.pdf")

    chunks = chunk_document(
        pages,
        method="recursive",
        chunk_size=500
    )

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        print(f"Embedding {i + 1}/{len(chunks)}...")

        chunk["embedding"] = create_embedding(
            chunk["text"]
        )

    # Save everything
    with open(
        "data/embedded_chunks.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            ensure_ascii=False
        )

    print("\nSaved successfully!")
    print("File: data/embedded_chunks.json")