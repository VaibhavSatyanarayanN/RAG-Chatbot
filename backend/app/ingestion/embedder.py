from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embedding(chunks):

    texts = [c["text"] for c in chunks]

    embeddings = model.encode(texts,batch_size=32, show_progress_bar=True)

    return embeddings