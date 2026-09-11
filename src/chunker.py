import re


# Topics that are clearly meaningful boundaries
SUBSECTIONS = [
    "Arrays",
    "Linked Lists",
    "Stacks",
    "Queues",
    "Trees",
    "Graphs",
    "Hash Tables",

    "Sorting Algorithms:",
    "Searching Algorithms:",

    "Dynamic Programming",
    "Greedy Algorithms",
    "Divide and Conquer",
    "String Algorithms",

    "Structural patterns",
    "Design patterns",
    "Object-oriented design principles",

    "Relational databases (SQL)",
    "NoSQL databases",
    "Indexing",
    "Transactions",
    "ACID properties",

    "Programming paradigms",
    "Memory management",
    "Concurrency",
    "Asynchronous programming",
    "Error handling",

    "Client-server architecture",
    "RESTful architecture",
    "Service-Oriented Architecture (SOA)",
    "Message Queuing",
    "Microservices",
    "Event-Driven Architecture (EDA)",
    "Layered Architecture",

    "Problem-solving strategies",
    "Coding techniques",
    "Coding best practices",
    "Time and space complexity analysis",
    "Debugging",
    "Optimization",
]


def section_chunking(pages):

    full_text = "\n".join(
        page["text"]
        for page in pages
    )

    # --------------------------------------------------
    # STEP 1
    # Find major sections
    # --------------------------------------------------

    major_pattern = r"(?m)^\s*(\d+)\.\s+(.+)$"

    major_matches = list(
        re.finditer(
            major_pattern,
            full_text
        )
    )

    final_chunks = []

    # --------------------------------------------------
    # STEP 2
    # Process every major section
    # --------------------------------------------------

    for major_index, major_match in enumerate(
        major_matches
    ):

        major_number = major_match.group(1)
        major_name = major_match.group(2).strip()

        major_start = major_match.start()

        if major_index + 1 < len(major_matches):
            major_end = major_matches[
                major_index + 1
            ].start()
        else:
            major_end = len(full_text)

        major_text = full_text[
            major_start:major_end
        ].strip()

        # --------------------------------------------------
        # STEP 3
        # Find valid subsection headings
        # --------------------------------------------------

        escaped_topics = [
            re.escape(topic)
            for topic in SUBSECTIONS
        ]

        subsection_pattern = (
            r"(?m)^\s*("
            + "|".join(escaped_topics)
            + r")\s*$"
        )

        subsection_matches = list(
            re.finditer(
                subsection_pattern,
                major_text,
                re.IGNORECASE
            )
        )

        # --------------------------------------------------
        # STEP 4
        # If there are no useful subsections,
        # keep the entire major section.
        # --------------------------------------------------

        if not subsection_matches:

            final_chunks.append({
                "section": (
                    f"{major_number}. "
                    f"{major_name}"
                ),
                "text": major_text
            })

            continue

        # --------------------------------------------------
        # STEP 5
        # Keep content BEFORE the first subsection.
        # This prevents data from being lost.
        # --------------------------------------------------

        prefix = major_text[
            :subsection_matches[0].start()
        ].strip()

        if prefix:

            final_chunks.append({
                "section": (
                    f"{major_number}. "
                    f"{major_name}"
                ),
                "text": prefix
            })

        # --------------------------------------------------
        # STEP 6
        # Create subsection chunks
        # --------------------------------------------------

        subsection_chunks = []

        for i, subsection_match in enumerate(
            subsection_matches
        ):

            subsection_name = (
                subsection_match.group(1)
            )

            start = subsection_match.start()

            if i + 1 < len(subsection_matches):
                end = subsection_matches[
                    i + 1
                ].start()
            else:
                end = len(major_text)

            subsection_text = major_text[
                start:end
            ].strip()

            subsection_chunks.append({
                "section": (
                    f"{major_number}. "
                    f"{major_name} → "
                    f"{subsection_name}"
                ),
                "text": subsection_text
            })

        # --------------------------------------------------
        # STEP 7
        # Don't create tiny chunks.
        #
        # If a subsection is smaller than 100 chars,
        # merge it with the next subsection.
        # --------------------------------------------------

        merged_chunks = []

        i = 0

        while i < len(subsection_chunks):

            current = subsection_chunks[i]

            if (
                len(current["text"]) < 100
                and i + 1 < len(subsection_chunks)
            ):

                next_chunk = subsection_chunks[i + 1]

                current["text"] += (
                    "\n\n"
                    + next_chunk["text"]
                )

                current["section"] += (
                    " + "
                    + next_chunk["section"].split(
                        " → "
                    )[-1]
                )

                i += 2

            else:

                merged_chunks.append(
                    current
                )

                i += 1

        final_chunks.extend(
            merged_chunks
        )

    return final_chunks


def chunk_document(
    pages,
    method="section"
):

    if method != "section":

        raise ValueError(
            "For now, use method='section'."
        )

    section_chunks = section_chunking(
        pages
    )

    document_chunks = []

    for chunk_index, chunk in enumerate(
        section_chunks
    ):

        document_chunks.append({

            "id":
                f"section-{chunk_index}",

            "text":
                chunk["text"],

            "page_number":
                None,

            "chunk_index":
                chunk_index,

            "chunking_method":
                method,

            "section":
                chunk["section"]
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

    print("\nCHUNK SIZES:")

    for chunk in chunks:

        print(
            f"{chunk['id']} | "
            f"{chunk['section']} | "
            f"{len(chunk['text'])} characters"
        )

    print("\nCHUNK DETAILS:")

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

        print(
            chunk["text"]
        )