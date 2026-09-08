from parser import parse_pdf
from chunker import chunk_document
from embeddings import create_embedding


if __name__ == "__main__":

    # -----------------------------
    # Step 1: Parse PDF
    # -----------------------------

    pages = parse_pdf("data/demopdf.pdf")

    print(f"Total pages: {len(pages)}")


    # -----------------------------
    # Step 2: Create chunks
    # -----------------------------

    chunks = chunk_document(
        pages,
        method="recursive",
        chunk_size=500
    )

    print(f"Total chunks: {len(chunks)}")


    # -----------------------------
    # Step 3: Create embeddings
    # -----------------------------

    for i, chunk in enumerate(chunks):

        print(
            f"Creating embedding {i + 1}/{len(chunks)}..."
        )

        chunk["embedding"] = create_embedding(
            chunk["text"]
        )


    # -----------------------------
    # Step 4: Inspect result
    # -----------------------------

    print("\n" + "=" * 80)
    print("FIRST EMBEDDED CHUNK")
    print("=" * 80)

    first_chunk = chunks[0]

    print("\nID:")
    print(first_chunk["id"])

    print("\nPAGE:")
    print(first_chunk["page_number"])

    print("\nCHUNK INDEX:")
    print(first_chunk["chunk_index"])

    print("\nMETHOD:")
    print(first_chunk["chunking_method"])

    print("\nTEXT:")
    print(first_chunk["text"])

    print("\nVECTOR DIMENSION:")
    print(len(first_chunk["embedding"]))

    print("\nFIRST 10 VECTOR VALUES:")
    print(first_chunk["embedding"][:10])