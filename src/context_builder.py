def build_context(results):

    context_parts = []

    for i, match in enumerate(results["matches"]):

        metadata = match.get("metadata", {})

        text = metadata.get("text", "")
        page = metadata.get("page_number")
        chunk = metadata.get("chunk_index")

        context_parts.append(
            f"""
[Source {i + 1}]
Page: {page}
Chunk: {chunk}
Similarity Score: {match["score"]}

{text}
"""
        )

    return "\n".join(context_parts)