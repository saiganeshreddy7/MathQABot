from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings

# ---- CONFIG ----
COLLECTION_NAME = "qa_math"
EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"
TOP_K = 3
THRESHOLD = 0.80  # cosine similarity threshold

# ---- Setup ----
client = QdrantClient(url="http://localhost:6333")
embedding_fn = HuggingFaceEmbeddings(model_name=EMBED_MODEL)


def search_qa(query: str, top_k: int = TOP_K, threshold: float = THRESHOLD):
    # 1. Embed query using HuggingFace embeddings
    query_vec = embedding_fn.embed_query(query)

    # 2. Search in Qdrant using the updated query_points method
    results = client.query_points(
        collection_name=COLLECTION_NAME, query=query_vec, limit=top_k
    ).points

    # 3. Filter by threshold
    matches = [r for r in results if r.score >= threshold]

    # 4. Format results
    if not matches:
        return 0

    formatted = []
    for i, r in enumerate(matches, start=1):
        q = r.payload.get("question", "")
        a = r.payload.get("answer", "")
        formatted.append(f"question-{i}: {q}\nanswer-{i}: {a}\n")

    return "\n".join(formatted)


# # ---- Example Usage ----
# # ---- Example Usage ----
# if __name__ == "__main__":
#     user_q = """
#             Linda bought two coloring books at $4 each, 4 packs of peanuts at $1.50 each pack, and one stuffed animal. She gave the cashier $25 and got no change. How much does a stuffed animal cost?"""
#     print(search_qa(user_q))
