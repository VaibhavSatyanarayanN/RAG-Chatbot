from controller.query_search import query_search
from fastapi import FastAPI
from llm.generate_ans import generate_answer
from llm.propmpts import build_prompt
from retrival.vector_strore import semantic_search
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",   # React
    "http://127.0.0.1:3000",
    "http://localhost:5173",   # Vite
    # Add your deployed frontend URL here
    "file:///D:/Self/Python_LLM/RAG_Chatbot/frontend/index.html"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allowed origins
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, PUT, DELETE etc.
    allow_headers=["*"],          # all headers
)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/query")
async def query_endpoint(request: QueryRequest):

    query = request.query

    answer=query_search(query)

    return {
        "query": query,
        "answer": answer
    }