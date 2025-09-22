import asyncio
# from unittest import result
from fastmcp import Client  
import json

client = Client("http://localhost:8001/mcp")


async def call_tool(query: str):
    async with client:
        result = await client.call_tool("enrich_query", {"query": query})
        # Extract the exact same JSON data structure
        final_data = []
        for content in result.content:
            if hasattr(content, "text"):
                # Parse back to original format
                final_data.append(json.loads(content.text))
        # print(result)
        return final_data


# if __name__ == "__main__":
#     query = "what is 2 + 2?"
#     results = asyncio.run(call_tool(query))
#     print(json.dumps(results, indent=2))