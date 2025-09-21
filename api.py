# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
# import asyncio

from workflow import workflow

# Initialize FastAPI app
app = FastAPI(
    title="Math Q&A API",
    description="API for handling math queries with workflow integration",
    version="1.0.0",
)


# ---- Request/Response Schemas ----
class QueryRequest(BaseModel):
    conv_id: Optional[str] = None
    query: str


class QueryResponse(BaseModel):
    conv_id: str
    unique_id: str
    query: str
    answer: str


# ---- Routes ----
@app.post("/ask", response_model=List[QueryResponse])
async def ask_math(request: QueryRequest):
    """
    Endpoint to ask a math question.
    - If conv_id is None, a new conversation is created.
    - If conv_id exists, it appends to that conversation.
    """
    response = await workflow(request.conv_id, request.query)
    return response


# ---- Health Check ----
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running"}
