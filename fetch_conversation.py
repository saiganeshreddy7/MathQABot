# fetch_conversation.py

from typing import Optional, Dict, Any
from database_config import CONVERSATION_COLLECTION


async def get_conversation_by_id(conversation_id: Optional[str]) -> Dict[str, Any]:
    """
    Fetch a conversation record by conversation_id from MongoDB.

    Args:
        conversation_id (Optional[str]): ID of the conversation. If None, return empty conversation.

    Returns:
        Dict: {
            "conversation_id": str or None,
            "conversations": List[Dict[question, answer]]
        }
    """
    if not conversation_id:
        return {"conversation_id": None, "conversations": []}

    record = await CONVERSATION_COLLECTION.find_one(
        {"conversation_id": conversation_id},
        {"_id": 0}  # exclude MongoDB internal _id
    )

    if not record:
        return {"conversation_id": conversation_id, "conversations": []}

    return record


# # Example usage:
# import asyncio
# conv_data = asyncio.run(get_conversation_by_id("conv_79594010"))
# print(conv_data)
