def build_prompt(context, question):

    prompt = f"""
You are an AI assistant answering questions using the provided context.

Use ONLY the information provided in the context.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided document."

CONTEXT:
--------------------
{context}
--------------------

QUESTION:
{question}

ANSWER:
"""

    return prompt