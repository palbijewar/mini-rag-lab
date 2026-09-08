from embeddings import create_embedding
from pinecone_client import index
from context_builder import build_context
from prompt import build_prompt


def retrieve(query: str, top_k: int = 5):

    query_embedding = create_embedding(query)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return results


if __name__ == "__main__":

    query = "What are the most important data structures for SDE interviews?"

    results = retrieve(
        query=query,
        top_k=5
    )

    context = build_context(results)

    prompt = build_prompt(
        context=context,
        question=query
    )

    print("\n" + "=" * 80)
    print("PROMPT THAT WILL BE SENT TO THE LLM")
    print("=" * 80)

    print(prompt)