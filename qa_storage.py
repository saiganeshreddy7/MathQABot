import uuid
from datetime import datetime
from database_config import QANDA_COLLECTION


def generate_short_uuid() -> str:
    """Generate a short, human-readable UUID"""
    return str(uuid.uuid4())[:8]  # first 8 chars of UUID


async def create_qa_record(question: str, answer: str):
    """
    Create a Q&A record with unique_id and default rating,
    insert it into MongoDB, and return the inserted record.
    """
    # Build record structure
    record = {
        "unique_id": generate_short_uuid(),
        "question": question,
        "answer": answer,
        "rating": {"value": "unrated", "description": None},
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    # Print for verification
    print("Constructed record:", record)

    # Insert into MongoDB
    result = await QANDA_COLLECTION.insert_one(record)
    print("Inserted record ID:", result.inserted_id)

    # Optionally fetch the inserted document
    inserted_record = await QANDA_COLLECTION.find_one({"_id": result.inserted_id})

    # Return as JSON-like dict
    return inserted_record


# # Example usage:
# import asyncio
# import json

# question = "What is 2 + 2?"
# answer = "2 + 2 equals 4."
# inserted = asyncio.run(create_qa_record(question, answer))
# print(json.dumps(inserted, indent=4,default=str))
