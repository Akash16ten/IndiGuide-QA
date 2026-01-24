from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
import requests

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

# ---------- Ask user a question ----------
query = input("Ask a question about the SIRE scheme: ")

# ---------- Embed the query ----------
query_embedding = embedder.encode([query])

# ---------- Retrieve relevant chunks ----------
k = 4
_, indices = index.search(np.array(query_embedding), k)

retrieved_chunks = []
for idx in indices[0]:
    doc = documents[idx]
    retrieved_chunks.append(
        f"[SECTION: {doc['section']}]\n{doc['text']}"
    )

context = "\n\n".join(retrieved_chunks)

# ---------- Build prompt ----------
prompt = f"""
You are an assistant answering questions using official government information.

Use ONLY the context below to answer.
If the answer is not present, say you do not have sufficient information.

Context:
{context}

Question:
{query}

Answer in clear, simple language.
Mention the relevant section names.
"""


# ---------- Call local LLM via Ollama (HTTP API) ----------
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "gemma:2b",
        "prompt": prompt,
        "stream": False
    },
    timeout=120
)

print("\nANSWER:\n")

if response.status_code == 200:
    print(response.json()["response"])
else:
    print("Error from Ollama:", response.text)
