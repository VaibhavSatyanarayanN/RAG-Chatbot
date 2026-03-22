import os
import sys



# Ensure the repository root is on sys.path so the app package can be imported when running the test directly.
# ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
# if ROOT_DIR not in sys.path:
#     sys.path.insert(0, ROOT_DIR)

import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from app.retrival.vector_strore import semantic_search,normalize
from app.llm.generate_ans import generate_answer
from app.llm.propmpts import build_prompt

# Load FAISS index
# index = faiss.read_index("../vectorstore/faiss_index")

model = SentenceTransformer("all-MiniLM-L6-v2")

def search():
    index = faiss.read_index("../vectorstore/faiss_index")
    with open("../vectorstore/metadata.json", "r") as f:
        chunks = json.load(f)

    while True:
        query = input("\nAsk a question (or 'exit'): ")

        if query.lower() == "exit":
            break

        # Step 1: Retrieve
        retrieved_chunks = semantic_search(query, index, chunks, model)

        # Step 2: Build prompt
        context_chunks = [chunk["text"] for chunk in retrieved_chunks]
        prompt = build_prompt(query, context_chunks)

        # Step 3: Generate answer
        answer = generate_answer(prompt)

        print("\n🤖 Answer:\n")
        print(answer,"Final ans")

if __name__ == "__main__":
    search()