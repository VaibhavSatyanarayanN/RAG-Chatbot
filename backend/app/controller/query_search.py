import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from retrival.vector_strore import semantic_search,normalize
from llm.generate_ans import generate_answer
from llm.propmpts import build_prompt

# Load FAISS index
# index = faiss.read_index("../vectorstore/faiss_index")

model = SentenceTransformer("all-MiniLM-L6-v2")

def query_search(query):
    index = faiss.read_index("../vectorstore/faiss_index")
    with open("../vectorstore/metadata.json", "r") as f:
        chunks = json.load(f)

    # Step 1: Retrieve
    retrieved_chunks = semantic_search(query, index, chunks, model)

    # Step 2: Build prompt
    context_chunks = [chunk["text"] for chunk in retrieved_chunks]
    prompt = build_prompt(query, context_chunks)

    # Step 3: Generate answer
    answer = generate_answer(prompt)

    print("\n🤖 Answer:\n")
    print(answer)
    return answer