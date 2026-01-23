from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ---------- Paths ----------
BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_FILE = BASE_DIR / "data" / "sire_clean.txt"
VECTOR_DIR = BASE_DIR / "vectorstore"
VECTOR_DIR.mkdir(exist_ok=True)

# ---------- Load cleaned text ----------
text = CLEAN_FILE.read_text(encoding="utf-8")

# ---------- Split by sections ----------
sections = text.split("[SECTION:")
documents = []

for sec in sections:
    if not sec.strip():
        continue

    header, content = sec.split("]", 1)
    section_name = header.strip()
    content = content.strip()

    # Chunk long sections
    chunk_size = 500
    for i in range(0, len(content), chunk_size):
        chunk = content[i:i + chunk_size]
        documents.append({
            "section": section_name,
            "text": chunk
        })

# ---------- Load embedding model ----------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- Create embeddings ----------
texts = [doc["text"] for doc in documents]
embeddings = model.encode(texts)

# ---------- Store in FAISS ----------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# ---------- Save vector index ----------
faiss.write_index(index, str(VECTOR_DIR / "sire.index"))

# ---------- Save metadata ----------
import json
with open(VECTOR_DIR / "sire_metadata.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=2)

print(f"Embedding complete — {len(documents)} chunks stored")
