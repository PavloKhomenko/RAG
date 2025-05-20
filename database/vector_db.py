from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, Filter, FieldCondition, MatchValue
from typing import Optional, List, Union
from uuid import uuid4
import datetime

class VectorDB:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "embeddings",
        vector_size: int = 512
    ):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self._create_collection()

    def _create_collection(self):
        if self.collection_name not in [c.name for c in self.client.get_collections().collections]:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE)
            )

    def add_embedding(
        self,
        type_: str,
        embedding: List[float],
        id_: Optional[str] = None,
        **kwargs
    ):
        payload = {"type": type_}

        if type_ == "article":
            payload.update({
                "title": kwargs.get("title"),
                "text": kwargs.get("text"),
                "url": kwargs.get("url"),
                "date": kwargs.get("date"),
            })
        elif type_ == "image":
            payload.update({
                "image_url": kwargs.get("image_url"),
                "caption": kwargs.get("caption"),
            })
        elif type_ == "chat":
            payload.update({
                "role": kwargs.get("role"),
                "content": kwargs.get("content"),
                "timestamp": kwargs.get("timestamp") or datetime.datetime.utcnow().isoformat()
            })
        else:
            raise ValueError(f"Unknown type: {type_}")

        point = PointStruct(
            id=id_ or str(uuid4()),
            vector=embedding,
            payload=payload
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def get_embedding(self, id_: Union[int, str]) -> Optional[dict]:
        result = self.client.retrieve(collection_name=self.collection_name, ids=[id_])
        return result[0].dict() if result else None

    def search(self, embedding: List[float], top_k: int = 5, type_: Optional[str] = None) -> List[dict]:
        filter_ = None
        if type_:
            filter_ = Filter(
                must=[FieldCondition(key="type", match=MatchValue(value=type_))]
            )
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=top_k,
            query_filter=filter_
        )
        return [r.payload for r in results]

    def search_articles(self, embedding: List[float], top_k: int = 5) -> List[dict]:
        return self.search(embedding, top_k=top_k, type_="article")

    def get_all_by_type(self, type_: str) -> List[dict]:
        filter_ = Filter(
            must=[FieldCondition(key="type", match=MatchValue(value=type_))]
        )
        scroll = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=filter_,
            limit=1000,
            with_payload=True
        )
        return [point.payload for point in scroll[0]]
    
    def clear(self, type_: str):
        filter_ = Filter(
            must=[FieldCondition(key="type", match=MatchValue(value=type_))]
        )
        self.client.delete(
            collection_name=self.collection_name,
            points_selector={"filter": filter_}
        )

    def close(self):
        self.client.close()
