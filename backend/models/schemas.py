from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    images: list[dict]
    sources: list[dict]
