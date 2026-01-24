# IndiGuide-QA 
*A Retrieval-Augmented Generation (RAG) system for Indian Government Schemes*

## Overview
IndiGuide-QA is an AI-powered question-answering system that allows users to ask natural language questions about Indian government schemes and receive accurate, grounded answers directly from official government websites.

The system uses **Retrieval-Augmented Generation (RAG)** to ensure answers are:
- Based only on official data
- Free from hallucinations
- Transparent and explainable

Currently, the project is implemented using data from the **SERB International Research Experience (SIRE)** scheme.

---

## How It Works

1. **Web Scraping**
   - Scrapes official government webpages
   - Extracts raw textual content

2. **Data Cleaning & Structuring**
   - Removes navigation menus and irrelevant content
   - Organizes information into logical sections (Eligibility, Objectives, Guidelines, etc.)

3. **Chunking & Embeddings**
   - Splits content into manageable chunks
   - Converts chunks into vector embeddings using Sentence Transformers

4. **Vector Search (Retrieval)**
   - Uses FAISS for semantic similarity search
   - Retrieves the most relevant chunks for a given user query

5. **Answer Generation**
   - Passes retrieved context to a local LLM (via Ollama)
   - Generates a concise, human-readable answer grounded in the source data

---

## Tech Stack

- **Language**: Python  
- **Embeddings**: SentenceTransformers (`all-MiniLM-L6-v2`)  
- **Vector Database**: FAISS  
- **LLM**: Local LLM via Ollama (`gemma:2b`)  
- **Parsing**: BeautifulSoup  
- **Architecture**: Layered, Retrieval-Augmented Generation (RAG)

---

## Project Structure

RAG Agent/
│
├── scripts/
│ ├── scraper_sire.py # Scrapes government website
│ ├── clean_sire.py # Cleans and structures text
│ ├── embed_sire.py # Creates embeddings & FAISS index
│ └── rag_sire.py # End-to-end RAG pipeline
│
├── data/
│ ├── sire_page.txt
│ └── sire_clean.txt
│
├── vectorstore/
│ ├── sire.index
│ └── sire_metadata.json
│
└── README.md


---

## Future Enhancements

- Support for multiple government schemes and ministries
- Web-based user interface
- Citation highlighting per answer
- Confidence scoring for responses
- Cloud deployment

---

## Disclaimer
This project is for educational purposes. All information is sourced from publicly available government websites.
