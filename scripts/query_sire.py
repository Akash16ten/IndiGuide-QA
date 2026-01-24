from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

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
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- Ask user a question ----------
query = input("Ask a question about the SIRE scheme: ")

# ---------- Embed the query ----------
query_embedding = model.encode([query])

# ---------- Search vector DB ----------
k = 3  # number of top results
distances, indices = index.search(np.array(query_embedding), k)

print("\nTop relevant sections:\n")

for idx in indices[0]:
    doc = documents[idx]
    print(f"SECTION: {doc['section']}")
    print(doc["text"][:500])  # preview
    print("-" * 50)