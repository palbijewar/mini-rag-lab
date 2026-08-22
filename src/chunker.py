from parser import parse_pdf


def fixed_size_chunking(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
):
    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start = end - chunk_overlap

    return chunks


def chunk_document(pages, chunk_size=500, chunk_overlap=100):
    document_chunks = []

    for page in pages:

        page_number = page["page_number"]
        text = page["text"]

        page_chunks = fixed_size_chunking(
            text=text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for chunk_index, chunk in enumerate(page_chunks):

            document_chunks.append({
                "id": f"page-{page_number}-chunk-{chunk_index}",
                "text": chunk,
                "page_number": page_number,
                "chunk_index": chunk_index
            })

    return document_chunks


if __name__ == "__main__":

    pages = parse_pdf("data/demopdf.pdf")

    chunks = chunk_document(
        pages,
        chunk_size=500,
        chunk_overlap=100
    )

    print(f"\nTOTAL PAGES: {len(pages)}")
    print(f"TOTAL CHUNKS: {len(chunks)}")

    for chunk in chunks[:5]:

        print("\n" + "=" * 80)
        print(f"ID: {chunk['id']}")
        print(f"PAGE: {chunk['page_number']}")
        print(f"CHUNK INDEX: {chunk['chunk_index']}")
        print("=" * 80)

        print(chunk["text"])