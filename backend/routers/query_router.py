from fastapi import APIRouter
from models.schemas import QueryRequest, QueryResponse
from rag_logic.generator import generate_rag_response

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_rag(req: QueryRequest):
    return generate_rag_response(req.query)
