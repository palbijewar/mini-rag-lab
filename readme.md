````markdown
# 🧠 Mini RAG Lab — Learn RAG & LLMs From Scratch

A small, hands-on **Retrieval-Augmented Generation (RAG)** project built without LangChain or other RAG frameworks.

The purpose of this project is not to build the most production-ready RAG system.

The purpose is to **understand what actually happens inside a RAG pipeline**.

Instead of hiding everything behind frameworks, this project implements the major components step-by-step so you can see:

- How a PDF becomes text
- How text is cleaned
- How documents are chunked
- What embeddings are
- What embedding dimensions mean
- How vectors represent text
- How cosine similarity works
- How a vector database works
- How Pinecone stores and retrieves vectors
- How a user's query becomes an embedding
- How Top-K retrieval works
- How retrieved context is constructed
- How prompts are built
- How an LLM generates the final answer
- How all of these pieces come together to form a RAG system

---

# 🚀 What is RAG?

**RAG = Retrieval-Augmented Generation**

A normal LLM answers a question using information available to the model.

A RAG system first retrieves relevant information from an external knowledge source and then gives that information to the LLM as context.

The basic flow is:

```text
User Question
      ↓
Create Query Embedding
      ↓
Search Vector Database
      ↓
Retrieve Relevant Chunks
      ↓
Build Context
      ↓
Build Prompt
      ↓
Send Prompt to LLM
      ↓
Generate Answer
````

In this project, the knowledge source is a PDF.

---

# 🎯 Why This Project Exists

There are many tutorials that show:

```python
chain = RetrievalQA(...)
```

and everything magically works.

That's useful when you want to build something quickly, but it doesn't necessarily teach you what is happening underneath.

This project takes the opposite approach.

We manually build the pipeline:

```text
PDF
 ↓
Parser
 ↓
Cleaner
 ↓
Chunker
 ↓
Embedding Model
 ↓
Vector Database
 ↓
Retriever
 ↓
Context Builder
 ↓
Prompt
 ↓
LLM
 ↓
Answer
```

The goal is to understand each box before using abstractions such as:

* LangChain
* LlamaIndex
* Haystack
* Agent frameworks
* Managed RAG platforms

---

# 🏗️ Architecture

```text
                    ┌───────────────┐
                    │      PDF      │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │  PDF Parser   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │    Cleaner    │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │    Chunker    │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │  Embeddings   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │   Pinecone    │
                    │ Vector Store  │
                    └───────┬───────┘
                            ↑
                            │
User Question ──→ Embedding Model
                            │
                            ↓
                    ┌───────────────┐
                    │ Vector Search │
                    └───────┬───────┘
                            ↓
                       Top-K Chunks
                            ↓
                    ┌───────────────┐
                    │Context Builder│
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ Prompt Builder│
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │      LLM      │
                    └───────┬───────┘
                            ↓
                       Final Answer
```

---

# 📁 Project Structure

```text
mini-rag-lab/
│
├── data/
│   ├── demopdf.pdf
│   └── embedded_chunks.json
│
├── src/
│   ├── parser.py
│   ├── cleaner.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── similarity.py
│   ├── save_embeddings.py
│   ├── embed_chunks.py
│   ├── pinecone_client.py
│   ├── reset_pinecone.py
│   ├── upsert_vectors.py
│   ├── retrieve.py
│   ├── context_builder.py
│   ├── prompt.py
│   └── llm.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🛠️ Tech Stack

* **Python**
* **PyPDF** — PDF text extraction
* **OpenAI-compatible SDK** — communicating with embedding/LLM APIs
* **OpenRouter** — API routing for models
* **text-embedding-3-small** — embedding model
* **Pinecone** — vector database
* **python-dotenv** — environment variables

No LangChain is required.

---

# ⚙️ Setup

## 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd mini-rag-lab
```

---

## 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it:

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the **project root**:

```env
OPENAI_API_KEY=your_openrouter_api_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1

PINECONE_API_KEY=your_pinecone_api_key
```

### Important

Never commit `.env` to GitHub.

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

# 📄 Step 1 — PDF Parsing

Start with:

```bash
PYTHONPATH=src python src/parser.py
```

The parser uses `pypdf` to extract text from every page.

Conceptually:

```python
reader = PdfReader(file_path)

for page in reader.pages:
    text = page.extract_text()
```

The result becomes something like:

```text
[
    {
        "page_number": 1,
        "text": "..."
    },
    {
        "page_number": 2,
        "text": "..."
    }
]
```

### What to learn here

A PDF is not automatically clean text.

PDF extraction can produce:

```text
OverviewWelcome
DataStructures
aimto
```

instead of:

```text
Overview
Welcome
Data Structures
aim to
```

This is why preprocessing matters.

---

# 🧹 Step 2 — Text Cleaning

Run the parser and inspect the output.

The cleaner fixes common extraction problems such as:

* Missing spaces
* Concatenated headings
* Broken section boundaries
* Repeated PDF footer text
* Checklist formatting

The important idea is:

```text
Raw PDF text
      ↓
Cleaning
      ↓
More usable text
```

### Why does cleaning matter?

Bad text creates bad chunks.

Bad chunks create bad embeddings.

Bad embeddings create poor retrieval.

Therefore:

```text
Bad preprocessing
       ↓
Bad retrieval
       ↓
Bad RAG answer
```

---

# ✂️ Step 3 — Chunking

LLMs and embedding models don't normally receive an entire large document as one giant piece.

We divide the document into smaller pieces called **chunks**.

This project explores different chunking approaches, including:

* Fixed-size chunking
* Sentence-based chunking
* Recursive chunking
* Section-aware chunking

The final pipeline uses **section-aware chunking**.

Run:

```bash
PYTHONPATH=src python src/chunker.py
```

You can inspect:

```text
Chunk ID
Section
Chunk size
Chunking method
Text
```

---

# 🧠 What is a Chunk?

Suppose a document contains:

```text
1. Data Structures

Arrays
Linked Lists
Stacks
Queues
Trees
Graphs
Hash Tables
```

Instead of embedding the entire PDF, we can create meaningful chunks such as:

```text
1. Data Structures

Arrays...
Linked Lists...
Stacks...
Queues...
Trees...
Graphs...
Hash Tables...
```

The goal is to create chunks that contain enough context to be useful during retrieval.

---

# 📐 Chunk Size and Overlap

Another important concept is **chunk overlap**.

For example:

```text
Chunk 1
-------------------------
A B C D E F G
            ↑
            overlap
              ↓
Chunk 2
            F G H I J K
```

Overlap helps prevent important information from being lost at chunk boundaries.

However, larger chunks are not automatically better.

You are balancing:

```text
More context
     ↕
More noise
```

and:

```text
Small chunks
     ↕
Less context
```

---

# 🔢 Step 4 — Embeddings

Now we convert text into numbers.

For example:

```text
"How does binary search work?"
```

becomes something conceptually like:

```text
[0.0381, 0.0386, -0.0339, 0.0159, ...]
```

In this project the embedding contains:

```text
1536 numbers
```

This is called the **embedding dimension**.

---

# 🧩 What is an Embedding?

An embedding is a numerical representation of text that captures semantic relationships.

Conceptually:

```text
"How does binary search work?"
          ↓
      Embedding Model
          ↓
[0.03, 0.04, -0.02, ...]
```

Related sentences tend to have vectors that are closer together in vector space.

For example:

```text
"How does binary search work?"
            ↓
       [vector A]

"Explain searching a sorted array."
            ↓
       [vector B]
```

These should be more similar than:

```text
"How does binary search work?"
            ↓
       [vector A]

"How do I cook chicken curry?"
            ↓
       [vector C]
```

---

# 📊 Embedding Dimensions

An embedding model can produce vectors of different dimensions.

Examples include:

```text
384
512
768
1024
1536
3072
```

A larger dimension does **not automatically mean a better embedding**.

Higher dimensions can mean:

* More storage
* More memory
* More computation
* Potentially richer representation

But model quality matters more than simply choosing the largest number.

### Important rule

The vectors you compare/store must be compatible.

If your Pinecone index expects:

```text
1536 dimensions
```

you cannot upload a:

```text
1024-dimensional vector
```

---

# 🔢 Step 5 — Cosine Similarity

This project also implements cosine similarity manually.

The formula is:

```text
                  A · B
cosine(A,B) = ─────────────
              ||A|| ||B||
```

In Python:

```python
def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    return dot_product / (magnitude_a * magnitude_b)
```

---

# 🤔 Why Cosine Similarity?

We don't necessarily care about the absolute size of vectors.

We care about their **direction**.

Conceptually:

```text
          B
         /
        /
       /
      /
     A

Small angle → more similar
Large angle → less similar
```

A cosine similarity closer to:

```text
1 → very similar direction
0 → unrelated
-1 → opposite direction
```

For typical text embeddings, you will commonly see values in the positive range.

---

# 🔍 Step 6 — Manual Semantic Search

Before using Pinecone, try comparing embeddings manually.

For example:

```text
Query:
How can I search efficiently in a sorted list?

Documents:

1. Binary Search
2. Merge Sort
3. Hash Maps
```

Calculate:

```text
Query ↔ Binary Search
Query ↔ Merge Sort
Query ↔ Hash Maps
```

Then sort by similarity.

You should see the most semantically relevant document near the top.

This is an important learning step because it shows what a vector database is ultimately helping you do at scale.

---

# 🗄️ Step 7 — Pinecone

Instead of manually comparing every vector, we use a vector database.

This project uses:

```text
Pinecone
```

The index is configured with:

```text
Dimension: 1536
Metric: cosine
```

The basic idea is:

```text
Document Chunk
     ↓
Embedding
     ↓
Vector
     ↓
Pinecone
```

Each stored vector also contains metadata such as:

```text
id
text
chunk_index
chunking_method
section
```

---

# 📤 Step 8 — Generate and Upload Embeddings

Generate embeddings for all chunks:

```bash
PYTHONPATH=src python src/embed_chunks.py
```

This creates:

```text
data/embedded_chunks.json
```

Then upload them:

```bash
PYTHONPATH=src python src/upsert_vectors.py
```

You should see something similar to:

```text
Loaded 11 chunks
Prepared 11 vectors
Vectors uploaded successfully!
```

You can verify the Pinecone index with:

```bash
PYTHONPATH=src python src/pinecone_client.py
```

---

# 🔎 Step 9 — Retrieval

Now the interesting part begins.

The user asks:

```text
What are the most important data structures for SDE interviews?
```

We first convert the question into an embedding:

```text
User Question
      ↓
Embedding Model
      ↓
1536-dimensional vector
```

Then we send that vector to Pinecone:

```python
results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True
)
```

`top_k=5` means:

> Give me the five most similar vectors.

---

# 🏆 What is Top-K?

Top-K retrieval means selecting the K most relevant chunks.

For example:

```text
Query
 ↓
Vector Search
 ↓
1. Data Structures        0.57
2. Problem Solving        0.55
3. Databases              0.49
4. Algorithms             0.48
5. System Design          0.42
```

The score represents similarity.

### Important

Similarity does **not** mean factual correctness.

A high similarity score means:

> "This chunk appears semantically related to the query."

It does not necessarily mean:

> "This chunk contains the exact answer."

This distinction is extremely important when designing RAG systems.

---

# 🧱 Step 10 — Context Building

The retrieved chunks are turned into a context string.

Conceptually:

```text
[Source 1]

Data Structures...

[Source 2]

Algorithms...

[Source 3]

Databases...
```

This is what the LLM will receive as external knowledge.

The LLM does not query Pinecone directly in this simple architecture.

Instead:

```text
Pinecone
   ↓
Retrieved chunks
   ↓
Context
   ↓
Prompt
   ↓
LLM
```

---

# 📝 Step 11 — Prompt Construction

The context is inserted into a prompt.

The project uses instructions similar to:

```text
You are an AI assistant answering questions
using the provided context.

Use ONLY the information provided in the context.

If the answer cannot be found in the context, say:

"I don't have enough information in the provided document."
```

Then:

```text
CONTEXT:
--------------------
Retrieved chunks
--------------------

QUESTION:
User question

ANSWER:
```

---

# 🤖 Step 12 — LLM

Finally, the prompt is sent to an LLM.

The LLM receives:

```text
Instructions
     +
Retrieved Context
     +
User Question
```

and generates:

```text
Final Answer
```

This is the **Generation** part of Retrieval-Augmented Generation.

---

# 🔄 Complete RAG Pipeline

The complete process is:

```text
                OFFLINE / INGESTION
                ===================

PDF
 ↓
Parse
 ↓
Clean
 ↓
Chunk
 ↓
Embedding Model
 ↓
Vectors
 ↓
Pinecone


                ONLINE / QUERY
                ==============

User Question
 ↓
Query Embedding
 ↓
Pinecone Search
 ↓
Top-K Chunks
 ↓
Context Builder
 ↓
Prompt Builder
 ↓
LLM
 ↓
Answer
```

This distinction between **ingestion** and **query-time retrieval** is an important concept to understand.

---

# 🧪 Try Your Own Questions

Once everything is configured, edit the question inside:

```text
src/retrieve.py
```

For example:

```python
query = "What are the different types of trees?"
```

or:

```python
query = "What database concepts should I study?"
```

or:

```python
query = "What networking topics are included?"
```

Then run:

```bash
PYTHONPATH=src python src/retrieve.py
```

---

# 🧠 Things You Should Experiment With

This repository is intended to be modified.

Try changing:

### 1. Chunking strategy

Compare:

```text
Fixed-size
Sentence-based
Recursive
Section-aware
```

Ask:

> Which produces better retrieval?

---

### 2. Chunk size

Try:

```text
200
500
1000
1500
```

Then compare retrieval quality.

---

### 3. Top-K

Try:

```python
top_k=1
top_k=3
top_k=5
top_k=10
```

Ask:

> Does more context always produce a better answer?

It doesn't necessarily.

---

### 4. Questions

Try questions that:

* Have direct answers
* Require multiple chunks
* Are not present in the document
* Are only loosely related
* Are completely unrelated

This helps you understand retrieval failures.

---

# ⚠️ Important RAG Lessons

## 1. RAG does not eliminate hallucinations

RAG gives the LLM additional context.

It does not guarantee truth.

If retrieval is wrong:

```text
Bad retrieval
     ↓
Bad context
     ↓
Potentially bad answer
```

---

## 2. Better LLM ≠ automatically better RAG

A powerful LLM cannot recover information that was never retrieved.

```text
Garbage retrieval
      +
Great LLM
      =
Still potentially bad answer
```

Retrieval quality matters enormously.

---

## 3. Chunking is extremely important

The embedding model can only represent the chunk you give it.

If a chunk contains unrelated information:

```text
Topic A
Topic B
Topic C
Topic D
```

its embedding may become less useful for a specific query.

---

## 4. Similarity ≠ relevance

A semantically related chunk may still not contain the answer.

Vector search is a retrieval mechanism, not a reasoning mechanism.

---

## 5. Top-K is a tradeoff

Too few chunks:

```text
Not enough information
```

Too many chunks:

```text
Too much irrelevant context
```

The goal is useful context, not maximum context.

---

# 🧩 Why We Didn't Use LangChain

LangChain is extremely useful.

But for learning RAG, building the first version manually is valuable.

Instead of:

```python
chain.invoke(question)
```

you can see:

```text
Embedding
 ↓
Vector Search
 ↓
Retrieved Documents
 ↓
Context
 ↓
Prompt
 ↓
LLM
```

Once you understand those pieces, frameworks become much easier to learn.

You know what abstraction they are providing.

---

# 📚 Recommended Learning Path

If you're using this repository to learn GenAI, don't just run the project.

Study it in this order:

```text
1. What is an LLM?
        ↓
2. Tokens
        ↓
3. Embeddings
        ↓
4. Embedding dimensions
        ↓
5. Vector similarity
        ↓
6. Cosine similarity
        ↓
7. Vector databases
        ↓
8. Chunking
        ↓
9. Retrieval / Top-K
        ↓
10. Prompt engineering
        ↓
11. RAG
        ↓
12. RAG evaluation
        ↓
13. Hybrid search
        ↓
14. Reranking
        ↓
15. Agents / Tool Calling
```

---

# 🚀 What to Learn Next

Once you understand this project, the natural next topics are:

### RAG

* Hybrid search
* BM25
* Dense + sparse retrieval
* Reranking
* Metadata filtering
* Query rewriting
* Multi-query retrieval
* Parent-child retrieval
* Context compression
* RAG evaluation
* Precision / Recall
* Retrieval metrics

### LLMs

* Tokens
* Context windows
* Temperature
* Top-p
* System / user / assistant messages
* Structured output
* Function calling
* Tool calling
* Streaming
* Model selection

### Advanced GenAI

* Agents
* Tool use
* MCP
* Long-term memory
* Multimodal models
* Fine-tuning
* LoRA
* Evaluation
* Production RAG architecture

---

# 💡 A Useful Mental Model

Remember this:

```text
Embedding model
    =
Converts meaning → numbers


Vector database
    =
Finds similar numbers


Retriever
    =
Chooses useful information


Prompt
    =
Gives information + instructions to LLM


LLM
    =
Reasons over the provided information
     and generates language


RAG
    =
Retrieval + Generation
```

If you understand these six concepts, you understand the core of a basic RAG system.

---

# 🎓 Learning Goal

After completing this project, you should be able to explain:

### "What happens when a user asks a question to a RAG application?"

A good answer would be:

> The user's question is converted into an embedding using the same embedding model used for the document chunks. The query vector is sent to a vector database, which retrieves the most semantically similar chunks using a similarity metric such as cosine similarity. Those chunks are combined into context and inserted into a prompt along with the user's question. The prompt is then sent to an LLM, which generates the final answer using the retrieved context.

If you can explain that **without relying on a framework's terminology**, you understand the fundamental RAG pipeline.

---

# 🤝 Contributing

This project is intentionally simple and educational.

If you want to experiment:

* Try different chunking strategies
* Try different embedding models
* Compare vector databases
* Add metadata filtering
* Add reranking
* Add evaluation
* Add streaming responses
* Add a UI
* Replace the PDF parser
* Implement retrieval completely without Pinecone

Pull requests and learning experiments are welcome.

---

# ⭐ Final Note

The goal of this repository is not:

> "Build a complicated AI application."

The goal is:

> **Understand what is happening underneath an AI application.**

Start with the individual Python files.

Run them.

Print the intermediate results.

Change the parameters.

Break things intentionally.

Then fix them.

Once you understand the pipeline manually, frameworks like LangChain and LlamaIndex become tools you can choose to use—not black boxes you depend on.

---

## 🧠 Build it. Break it. Understand it.

**RAG becomes much easier when you stop treating it as magic and start treating it as a pipeline.**

````

### One thing I'd add to the repo

I'd also create a tiny **`LEARNING.md`** alongside the README. The README tells people *how to run it*, while `LEARNING.md` can contain the actual experiments/questions they should answer as they move through the code.

For example:

```markdown
# 🧪 RAG Learning Checklist

- [ ] Understand PDF parsing
- [ ] Inspect raw extracted text
- [ ] Understand why cleaning is necessary
- [ ] Compare different chunking strategies
- [ ] Understand chunk size and overlap
- [ ] Generate one embedding manually
- [ ] Understand embedding dimensions
- [ ] Compare two embeddings
- [ ] Implement cosine similarity manually
- [ ] Perform manual semantic search
- [ ] Understand Top-K retrieval
- [ ] Create a Pinecone index
- [ ] Upload vectors
- [ ] Retrieve vectors
- [ ] Build context
- [ ] Build the prompt
- [ ] Send context to an LLM
- [ ] Run the complete RAG pipeline
- [ ] Test questions that aren't in the PDF
- [ ] Experiment with Top-K
- [ ] Experiment with chunk sizes
- [ ] Understand retrieval failure
- [ ] Understand hallucination
- [ ] Explain the complete RAG pipeline without LangChain
````

