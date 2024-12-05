from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.dependencies import get_embedding_generator, get_model, get_vector_search
from app.services.rag_pipeline import rag_pipeline


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str


chat_router = APIRouter()


@chat_router.post("", response_model=QueryResponse)
async def chat(
    query_request: QueryRequest,
    vector_search=Depends(get_vector_search),
    embedding_generator=Depends(get_embedding_generator),
    model=Depends(get_model),
):
    """
    Chat endpoint using the RAG pipeline with injected dependencies.
    """
    try:
        user_query = query_request.query

        chatbot_response = rag_pipeline(
            [user_query], vector_search, embedding_generator, model
        )

        return QueryResponse(response=chatbot_response)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing the request: {str(e)} {str(e.with_traceback)}",
        )
