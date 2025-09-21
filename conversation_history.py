from typing import Optional, Dict
from database_config import CONVERSATION_COLLECTION


async def get_conversation_history(conversation_id: Optional[str]) -> Dict:
    """
    Fetch conversation history for given conversation_id.
    - If conversation_id is None, return empty history.
    - If conversation_id exists in DB, return its record.
    - If not found, also return empty history.
    """
    if not conversation_id:
        return {"conversation_id": None, "conversations": []}

    record = await CONVERSATION_COLLECTION.find_one(
        {"conversation_id": conversation_id},
        {"_id": 0},  # exclude MongoDB internal _id
    )

    if not record:
        return {"conversation_id": None, "conversations": []}
    conversations = record["conversations"]

    return conversations


# Example usage:
# import asyncio

# Case 1: New chat
# history = asyncio.run(get_conversation_history(None))
# -> {"conversation_id": None, "conversations": []}

# Case 2: Existing chat
# history = asyncio.run(get_conversation_history("conv_79594010"))
# -> {"conversation_id": "conv_1234abcd", "conversations": [{...}, {...}]}
# print(history)
