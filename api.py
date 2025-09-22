# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
# import asyncio

from workflow import workflow
from rate_answer import rate_answer
from fetch_conversation import get_conversation_by_id

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


class FeedbackRequest(BaseModel):
    unique_id: str
    value: str
    description: Optional[str] = None


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


@app.post("/feedback")
async def give_feedback(request: FeedbackRequest):
    """
    Endpoint to give feedback (rate answer) on a Q&A record.
    Updates the rating field in MongoDB.
    """
    try:
        await rate_answer(request.unique_id, request.value, request.description)
        return {"status": "success", "message": "Feedback recorded"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    

# ---- New endpoint: fetch conversation history ----
@app.get("/conversation/{conv_id}")
async def fetch_conversation(conv_id: str):
    """
    Fetch full conversation history for a given conversation ID.
    - Returns the conversation object with all Q&A turns.
    - If conv_id does not exist, returns empty conversations list.
    """
    try:
        conversation = await get_conversation_by_id(conv_id)
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch conversation: {str(e)}")
    

# ---- Health Check ----
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running"}
