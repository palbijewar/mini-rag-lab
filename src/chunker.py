import re


def section_chunking(pages):
    """
    Split the document into meaningful subsection chunks.

    Major sections:
        1. Data Structures
        2. Algorithms
        ...

    Within a major section, we also detect subsection headings such as:
        Sorting Algorithms
        Searching Algorithms
        String Algorithms
        Greedy Algorithms
        Dynamic Programming
    """

    full_text = "\n".join(
        page["text"]
        for page in pages
    )

    # --------------------------------------------------
    # STEP 1: Find major sections
    # --------------------------------------------------

    major_pattern = r"(?m)^\s*(\d+)\.\s+(.+)$"

    major_matches = list(
        re.finditer(major_pattern, full_text)
    )

    chunks = []

    for major_index, major_match in enumerate(major_matches):

        major_number = major_match.group(1)
        major_name = major_match.group(2).strip()

        major_start = major_match.start()

        if major_index + 1 < len(major_matches):
            major_end = major_matches[major_index + 1].start()
        else:
            major_end = len(full_text)

        major_text = full_text[
            major_start:major_end
        ].strip()

        # --------------------------------------------------
        # STEP 2: Find meaningful subsections
        # --------------------------------------------------

        subsection_pattern = (
            r"(?m)^\s*"
            r"(Sorting Algorithms|"
            r"Searching Algorithms|"
            r"String Algorithms|"
            r"Greedy Algorithms|"
            r"Divide and Conquer|"
            r"Dynamic Programming|"
            r"Structural patterns|"
            r"Design patterns|"
            r"Behavioral patterns|"
            r"Object-oriented design principles|"
            r"Scalability|"
            r"Distributed systems|"
            r"Microservices architecture|"
            r"Database design and optimization|"
            r"Indexing|"
            r"Transactions|"
            r"ACID properties|"
            r"NoSQL databases|"
            r"Networking|"
            r"Memory management|"
            r"Concurrency|"
            r"Asynchronous programming|"
            r"Error handling|"
            r"Functional programming|"
            r"Object-oriented programming \(OOP\)|"
            r"Design patterns|"
            r"Client-server architecture|"
            r"RESTful architecture|"
            r"Service-Oriented Architecture \(SOA\)|"
            r"Message Queuing|"
            r"Microservices|"
            r"Event-Driven Architecture \(EDA\)|"
            r"Layered Architecture|"
            r"Problem-solving strategies|"
            r"Coding techniques|"
            r"Coding best practices|"
            r"Time and space complexity analysis|"
            r"Debugging|"
            r"Optimization)"
            r"\s*$"
        )

        subsection_matches = list(
            re.finditer(
                subsection_pattern,
                major_text
            )
        )

        # --------------------------------------------------
        # STEP 3: If no subsections exist,
        # keep the major section as one chunk
        # --------------------------------------------------

        if not subsection_matches:

            chunks.append({
                "section": (
                    f"{major_number}. "
                    f"{major_name}"
                ),
                "text": major_text
            })

            continue

        # --------------------------------------------------
        # STEP 4: Create subsection chunks
        # --------------------------------------------------

        for subsection_index, subsection_match in enumerate(
            subsection_matches
        ):

            subsection_name = (
                subsection_match.group(1)
            )

            start = subsection_match.start()

            if (
                subsection_index + 1
                < len(subsection_matches)
            ):
                end = subsection_matches[
                    subsection_index + 1
                ].start()
            else:
                end = len(major_text)

            subsection_text = major_text[
                start:end
            ].strip()

            chunks.append({
                "section": (
                    f"{major_number}. "
                    f"{major_name} → "
                    f"{subsection_name}"
                ),
                "text": subsection_text
            })

    return chunks


def chunk_document(pages, method="section"):

    if method != "section":
        raise ValueError(
            "For now, use method='section'."
        )

    section_chunks = section_chunking(pages)

    document_chunks = []

    for chunk_index, chunk in enumerate(
        section_chunks
    ):

        document_chunks.append({
            "id": f"section-{chunk_index}",
            "text": chunk["text"],
            "page_number": None,
            "chunk_index": chunk_index,
            "chunking_method": method,
            "section": chunk["section"]
        })

    return document_chunks


if __name__ == "__main__":

    from parser import parse_pdf

    pages = parse_pdf(
        "data/demopdf.pdf"
    )

    chunks = chunk_document(
        pages,
        method="section"
    )

    print(
        f"\nTOTAL PAGES: {len(pages)}"
    )

    print(
        f"TOTAL CHUNKS: {len(chunks)}"
    )

    for chunk in chunks:

        print("\n" + "=" * 80)

        print(
            f"ID: {chunk['id']}"
        )

        print(
            f"SECTION: {chunk['section']}"
        )

        print(
            f"SIZE: {len(chunk['text'])} characters"
        )

        print("=" * 80)

        print(chunk["text"])