from fastapi import APIRouter
from memory.vector_memory import VectorMemory
from embeddings.text_embedder import TextEmbedder
from database.vector_db import VectorDB

router = APIRouter()

text_embedder = TextEmbedder()
db = VectorDB(vector_size=512)
vector_memory = VectorMemory(db=db, embedder=text_embedder)

@router.post("/clear")
async def clear_chat_history():
    vector_memory.clear()
    return {"detail": "Chat history cleared."}
