from pathlib import Path
import json
import numpy as np
import faiss
import requests
from sentence_transformers import SentenceTransformer


# ---------- Paths ----------
BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DIR = BASE_DIR / "vectorstore"

INDEX_FILE = VECTOR_DIR / "sire.index"
META_FILE = VECTOR_DIR / "sire_metadata.json"


# ---------- Load FAISS index ----------
index = faiss.read_index(str(INDEX_FILE))


# ---------- Load metadata ----------
with open(META_FILE, "r", encoding="utf-8") as f:
    documents = json.load(f)


# ---------- Load embedding model ----------
embedder = SentenceTransformer("all-MiniLM-L6-v2")


def answer_question(query: str) -> dict:
    """
    Takes a user question and returns a grounded answer
    using Retrieval-Augmented Generation (RAG).
    """

    # ---------- Embed query ----------
    query_embedding = embedder.encode([query])

    # ---------- Retrieve chunks ----------
    k = 6
    _, indices = index.search(np.array(query_embedding), k)

    retrieved_chunks = []
    source_sections = set()

    for idx in indices[0]:
        doc = documents[idx]
        retrieved_chunks.append(
            f"[SECTION: {doc['section']}]\n{doc['text']}"
        )
        source_sections.add(doc["section"])

    context = "\n\n".join(retrieved_chunks)

    # ---------- Prompt ----------
    prompt = f"""
You are an assistant answering questions using official government information.

Use the context below as the primary source to answer.
If the answer can be reasonably inferred from the context, answer clearly.
If the context truly does not contain the information, then say so.
If someone asks your name, Introduce yourself as IndiGuide QA and tell that you help in extracting valuable insights.

If an Eligibility section is present, extract eligibility criteria from it.

Context:
{context}

Question:
{query}

Answer in clear, simple language.
Combine information from multiple sections if needed.
Give a very detailed, complete answer using full sentences.
Mention the relevant section names.
Do NOT include headings like "ANSWER:" in your response.
Do NOT be brief.
"""


    # ---------- Call Ollama ----------
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma:2b",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    if response.status_code != 200:
        return {
            "answer": "Error generating answer from the language model.",
            "sources": []
        }

    data = response.json()

    return {
        "answer": data.get("response", "").strip(),
        "sources": list(source_sections)
    }


# ---------- CLI ----------
if __name__ == "__main__":
    q = input("Ask a question about the SIRE scheme: ")
    res = answer_question(q)

    print("\nANSWER:\n")
    print(res["answer"])
    print("\nSOURCES:")
    for s in res["sources"]:
        print("-", s)
