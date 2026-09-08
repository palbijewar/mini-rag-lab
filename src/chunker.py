from parser import parse_pdf
from cleaner import clean_text

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
        text = clean_text(page["text"])

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

         page_chunks = recursive_chunk(
        text=text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
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

def recursive_chunk(text, chunk_size=500, chunk_overlap=100):
    separators = [
    "\n\n",
    "\n",
    ". ",
    " "
]

    chunks = []

    def split_text(text, separators):
        if len(text) <= chunk_size:
            return [text]

        separator = separators[0]
        remaining_separators = separators[1:]

        parts = text.split(separator)

        result = []
        current = ""

        for part in parts:
            candidate = current + separator + part if current else part

            if len(candidate) <= chunk_size:
                current = candidate
            else:
                if current:
                    result.append(current)

                current = part

        if current:
            result.append(current)

        final_chunks = []

        for chunk in result:
            if len(chunk) > chunk_size and remaining_separators:
                final_chunks.extend(
                    split_text(chunk, remaining_separators)
                )
            else:
                final_chunks.append(chunk)

        return final_chunks

    raw_chunks = split_text(text, separators)

    for i, chunk in enumerate(raw_chunks):
        if i == 0:
            chunks.append(chunk)
        else:
            previous = raw_chunks[i - 1]
            overlap = previous[-chunk_overlap:]
            chunks.append(overlap + " " + chunk)

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