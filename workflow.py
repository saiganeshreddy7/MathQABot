# import asyncio
import requests
# import sys


# ---- Imports ----
from math_content_validator import is_math_input, is_math_output
from vector_search import search_qa
from mcp_tool_client import call_tool
from conversation_history import get_conversation_history
from math_solver import solve_math
from qa_storage import create_qa_record
from conversation_storage import save_conversation_turn
from fastmcp import Client


# =========================================================
# Utility: Check Docker/Qdrant is running
# =========================================================
def check_qdrant():
    print("Checking if Qdrant is accessible at localhost:6333 ...")
    try:
        resp = requests.get("http://localhost:6333/healthz", timeout=3)
        if resp.status_code == 200:
            print("Qdrant is running and healthy ✅")
            return True
        else:
            print("Qdrant responded but not healthy ❌")
            return False
    except Exception as e:
        print("Error: Qdrant not reachable ❌", e)
        return False


# =========================================================
# Utility: Check MCP server is running
# =========================================================
async def check_mcp():
    print("Checking MCP server at localhost:8000/mcp ...")
    client = Client("http://localhost:8000/mcp")
    async with client:
        try:
            result = await client.call_tool("ping", {})
            pong_value = None
            if hasattr(result, "data"):
                pong_value = result.data
            elif (
                hasattr(result, "structured_content")
                and "result" in result.structured_content
            ):
                pong_value = result.structured_content["result"]

            if pong_value == "pong":
                print("MCP is running (pong pong pong) ✅")
                return True
            else:
                print("MCP ping failed ❌", result)
                return False
        except Exception as e:
            print("Error contacting MCP ❌", e)
            return False


# =========================================================
# Workflow Function
# =========================================================
async def workflow(conv_id: str, query: str):
    print("**" * 40)
    print(f"Starting workflow | conv_id={conv_id} | query='{query}'")

    # Step 1: Guardrails input
    if is_math_input(query) == 0:
        return {
            "conv_id": conv_id,
            "query": query,
            "answer": "❌ Please enter a mathematics question.",
        }

    # Step 2: Try retrieval from Qdrant
    context = search_qa(query)
    if context == 0:
        # fallback: MCP web search
        print("No relevant data in Qdrant. Falling back to MCP web search...")
        mcp_result = await call_tool(query)
        if mcp_result and hasattr(mcp_result, "structured_content"):
            context = str(mcp_result.structured_content)
        else:
            context = "No relevant data"

    print("Retrieved context:\n", context)

    # Step 3: Fetch conversation history
    conversations = await get_conversation_history(conv_id)
    print("Conversation history fetched:", conversations)

    # Step 4: Call LLM
    markdown_output = solve_math(
        query=query,
        context=context,
        conversation=conversations,
    )
    print("LLM produced output:\n", markdown_output[:300], "...")  # Print preview

    # Step 5: Guardrails output
    if is_math_output(markdown_output) == 0:
        return {
            "conv_id": conv_id,
            "query": query,
            "answer": "❌ Output failed guardrails: Not a valid math response.",
        }

    # Step 6: Save Q&A record
    record = await create_qa_record(query, markdown_output)
    query_final = record.get("question", query)
    answer_final = record.get("answer", markdown_output)
    unique_id = record.get("unique_id", None)  # 🔹 extract unique_id

    # Step 7: Save to conversation log
    conv_id = await save_conversation_turn(query_final, answer_final, conv_id)

    print("**" * 40)
    print("Workflow completed successfully ✅")

    # Step 8: Return final response
    return [
        {
            "conv_id": conv_id,
            "unique_id": unique_id,
            "query": query_final,
            "answer": answer_final,
        }
    ]


# =========================================================
# Main Entrypoint
# =========================================================
# if __name__ == "__main__":
#     # Check Qdrant first
#     if not check_qdrant():
#         print("Stopping: Qdrant is not ready ❌")
#         sys.exit(1)

#     # Check MCP server
#     ok = asyncio.run(check_mcp())
#     if not ok:
#         print("Stopping: MCP server not ready ❌")
#         sys.exit(1)

#     # Example query
#     test_conv_id = None
#     test_query = "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?"

#     response = asyncio.run(workflow(test_conv_id, test_query))
#     print("\nFinal Response:\n", response)
