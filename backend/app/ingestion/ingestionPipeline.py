import os
import sys

# Ensure the repository root is on sys.path so the app package can be imported when running the test directly.
# ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
# if ROOT_DIR not in sys.path:
#     sys.path.insert(0, ROOT_DIR)

import faiss
from embedder import create_embedding
import numpy as np
import json
from retrival.vector_strore import add_vectors, save
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdfs(folder_path):

    all_docs = []

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            path = os.path.join(folder_path, file)

            loader = PyPDFLoader(path)
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = file  # track file name

            all_docs.extend(docs)

    return all_docs

def chunk_documents(docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for doc_id, doc in enumerate(docs):
        split_chunks = splitter.split_text(str(doc))

        for chunk in split_chunks:
            chunks.append({
                "text": chunk,
                "doc_id": doc_id
            })

    return chunks

def ingestion_pipeline():

    print("Loading documents...")
    docs = load_pdfs("../../data")

    print("Chunking documents...")
    chunks = chunk_documents(docs)

    print(f"Total chunks: {len(chunks)}")

    print("Loading embedding model...")

    print("Creating embeddings...")
    embeddings = create_embedding(chunks)

    print("Storing in FAISS...")
    index = add_vectors( embeddings)

    print("Saving...")
    save(index, chunks)

    print("✅ Ingestion completed successfully!")

# Run
if __name__ == "__main__":
    ingestion_pipeline()