import json

import faiss
import numpy as np

dimension = 384

index = faiss.IndexFlatIP(dimension)

# faiss.write_index(index, "../vectorstore/faiss_index")
# index = faiss.read_index("../vectorstore/faiss_index")
# documents = []

def normalize(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms

def add_vectors( embeddings):
    vectors = np.array(embeddings).astype("float32") 
    vectors = normalize(vectors) 
    dimension = vectors.shape[1] 
    index = faiss.IndexFlatIP(dimension) 
    index.add(vectors) 
    return index

def save(index, chunks):

    faiss.write_index(index, "../../vectorstore/faiss_index")

    with open("../../vectorstore/metadata.json", "w") as f:
        json.dump(chunks, f)

def semantic_search(query, index, chunks, model, top_k=5):
    query_vec = model.encode([query])
    query_vec = normalize(np.array(query_vec).astype("float32"))

    distances, indices = index.search(query_vec, top_k)

    results = []
    for idx, score in zip(indices[0], distances[0]):
        chunk_info = chunks[idx]
        results.append({
            "text": chunk_info["text"],
            "doc_id": chunk_info["doc_id"],
            "score": float(score)
        })

    return results