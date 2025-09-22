# import asyncio
from fastmcp import Client

client = Client("http://localhost:8001/mcp")


async def call_tool(query: str):
    async with client:
        result = await client.call_tool("enrich_query", {"query": query})
        # print(result)
        return result


# if __name__ == "__main__":
#     query = "What is the capital of France?"
#     asyncio.run(call_tool(query))
