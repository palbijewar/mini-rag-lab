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

import re


def sentence_chunking(
    text: str,
    chunk_size: int = 500
):
    # Split text after ., !, or ?
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        # Skip empty sentences
        if not sentence.strip():
            continue

        # If adding this sentence exceeds chunk_size,
        # save the current chunk
        if len(current_chunk) + len(sentence) > chunk_size:

            if current_chunk:
                chunks.append(current_chunk.strip())

            current_chunk = sentence

        else:
            current_chunk += " " + sentence

    # Add the final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def chunk_document(
    pages,
    method="fixed",
    chunk_size=500,
    chunk_overlap=100
):
    document_chunks = []

    for page in pages:

        page_number = page["page_number"]
        text = page["text"]

        # Select chunking method
        if method == "fixed":

            page_chunks = fixed_size_chunking(
                text=text,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )

        elif method == "sentence":

            page_chunks = sentence_chunking(
                text=text,
                chunk_size=chunk_size
            )

        elif method == "recursive":

            page_chunks = recursive_chunking(
                text=text,
                chunk_size=chunk_size
            )

        else:
            raise ValueError(
                "Invalid method. Choose: fixed, sentence, or recursive"
            )

        # Add metadata to every chunk
        for chunk_index, chunk in enumerate(page_chunks):

            document_chunks.append({
                "id": f"page-{page_number}-chunk-{chunk_index}",
                "text": chunk,
                "page_number": page_number,
                "chunk_index": chunk_index,
                "chunking_method": method
            })

    return document_chunks

def recursive_chunking(
    text: str,
    chunk_size: int = 500,
    separators=None
):
    if separators is None:
        separators = [
            "\n\n",  # paragraph
            "\n",    # line
            ". ",    # sentence
            " ",     # word
            ""       # character fallback
        ]

    # Base case: text already fits
    if len(text) <= chunk_size:
        return [text.strip()]

    separator = separators[0]
    remaining_separators = separators[1:]

    # Final fallback: character splitting
    if separator == "":
        return [
            text[i:i + chunk_size]
            for i in range(0, len(text), chunk_size)
        ]

    parts = text.split(separator)

    chunks = []
    current_chunk = ""

    for part in parts:

        if not part.strip():
            continue

        # Add separator back while joining
        if current_chunk:
            candidate = current_chunk + separator + part
        else:
            candidate = part

        # Candidate fits inside chunk size
        if len(candidate) <= chunk_size:
            current_chunk = candidate

        else:
            # Save the current chunk first
            if current_chunk:
                chunks.append(current_chunk.strip())

            # This single part is still too big,
            # so recursively split it with smaller separators
            if len(part) > chunk_size:

                smaller_chunks = recursive_chunking(
                    part,
                    chunk_size,
                    remaining_separators
                )

                chunks.extend(smaller_chunks)
                current_chunk = ""

            else:
                current_chunk = part

    # Add the remaining chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

if __name__ == "__main__":

    pages = parse_pdf("data/demopdf.pdf")

    chunks = chunk_document(
        pages,
        method="recursive",
        chunk_size=500
    )

    print(f"\nTOTAL PAGES: {len(pages)}")
    print(f"TOTAL CHUNKS: {len(chunks)}")

    for chunk in chunks[:10]:

        print("\n" + "=" * 80)
        print(f"ID: {chunk['id']}")
        print(f"PAGE: {chunk['page_number']}")
        print(f"CHUNK INDEX: {chunk['chunk_index']}")
        print(f"METHOD: {chunk['chunking_method']}")
        print("=" * 80)

        print(chunk["text"])