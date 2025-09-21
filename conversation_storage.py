# conversation_writer.py

import uuid
from typing import Optional
from database_config import CONVERSATION_COLLECTION


def generate_conversation_id() -> str:
    """Generate a short unique conversation ID."""
    return f"conv_{uuid.uuid4().hex[:8]}"


async def save_conversation_turn(
    question: str, answer: str, conversation_id: Optional[str] = None
) -> str:
    """
    Save one Q&A turn into conversation history.
    - If conversation_id is None -> create new record with generated ID
    - Else -> append to existing record
    Returns the conversation_id (new or existing).
    """
    turn = {
        "question": question,
        "answer": answer,
    }

    if not conversation_id:
        # New conversation
        conversation_id = generate_conversation_id()
        new_record = {"conversation_id": conversation_id, "conversations": [turn]}
        await CONVERSATION_COLLECTION.insert_one(new_record)
        return conversation_id

    # Existing conversation -> update
    record = await CONVERSATION_COLLECTION.find_one(
        {"conversation_id": conversation_id}
    )

    if not record:
        # If ID doesn’t exist, treat it like new
        conversation_id = generate_conversation_id()
        new_record = {"conversation_id": conversation_id, "conversations": [turn]}
        await CONVERSATION_COLLECTION.insert_one(new_record)
        return conversation_id

    # Append to existing conversations
    await CONVERSATION_COLLECTION.update_one(
        {"conversation_id": conversation_id}, {"$push": {"conversations": turn}}
    )

    return conversation_id


# # Example usage:
# import asyncio
# # conv_id = asyncio.run(save_conversation_turn("What is 2+2?", "4", None))
# # Creates new conversation with conv_xxxx
# conv_id = "conv_79594010"
# result = asyncio.run(save_conversation_turn("What is 10*10?", "100", conv_id))
# # Finds conv_xxxx and appends new Q&A to conversations[]
