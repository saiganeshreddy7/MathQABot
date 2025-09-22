from datetime import datetime
from typing import Optional
from database_config import QANDA_COLLECTION


async def rate_answer(unique_id: str, value: str, description: Optional[str] = None) -> None:
    """
    Update the rating for a Q&A record in MongoDB.

    Args:
        unique_id (str): Unique ID of the Q&A record.
        value (str): Rating value (e.g., "good", "bad", "unrated").
        description (Optional[str]): Extra description for the rating.
    """
    update_doc = {
        "$set": {
            "rating": {
                "value": value,
                "description": description
            },
            "updatedAt": datetime.utcnow()
        }
    }

    result = await QANDA_COLLECTION.update_one(
        {"unique_id": unique_id},
        update_doc
    )

    if result.matched_count == 0:
        raise ValueError(f"No record found with unique_id={unique_id}")


# import asyncio

# # Example: rating an answer
# result = asyncio.run(rate_answer("8c30bed3", "good", "Clear explanation with steps"))
