from typing import List
from database.vector_db import VectorDB
from sentence_transformers import SentenceTransformer

class VectorMemory:
    def __init__(self, db: VectorDB, embedder: SentenceTransformer, top_k: int = 5):
        self.db = db
        self.embedder = embedder
        self.top_k = top_k

    def add_chat_message(self, role: str, content: str, timestamp: str = None):
        embedding = self.embedder.embed([content])[0].tolist()
        self.db.add_embedding(
            type_="chat",
            embedding=embedding,
            role=role,
            content=content,
            timestamp=timestamp
        )

    def retrieve_relevant_chats(self, query: str) -> List[str]:
        query_emb = self.embedder.embed([query])[0].tolist()
        results = self.db.search(
            embedding=query_emb,
            top_k=self.top_k,
            type_="chat"
        )
        return [f"{r['role']}: {r['content']}" for r in results if 'role' in r and 'content' in r]

    def clear(self):
        self.db.clear(type_="chat")
        pass    