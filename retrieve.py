import chromadb
from sentence_transformers import SentenceTransformer

from ingest import build_chunks

COLLECTION_NAME = "seo_guide"
DB_PATH = "chroma_db"

_model: SentenceTransformer | None = None
_collection = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=DB_PATH)
        _collection = client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def embed_and_store(chunks: list[dict]) -> None:
    model = _get_model()
    collection = _get_collection()

    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    batch_size = 500
    for i in range(0, len(texts), batch_size):
        collection.add(
            documents=texts[i : i + batch_size],
            embeddings=embeddings[i : i + batch_size],
            ids=ids[i : i + batch_size],
            metadatas=metadatas[i : i + batch_size],
        )
    print(f"Stored {len(texts)} chunks in ChromaDB.")


def query(text: str, k: int = 5) -> list[dict]:
    model = _get_model()
    collection = _get_collection()

    embedding = model.encode([text]).tolist()
    results = collection.query(
        query_embeddings=embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    return [
        {"text": doc, "source": meta["source"], "distance": round(dist, 4)}
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]


if __name__ == "__main__":
    chunks = build_chunks("documents")
    embed_and_store(chunks)

    test_query = "What percentage of Google searches were zero-click in 2025?"
    print(f"\nTest query: {test_query}\n")
    for i, result in enumerate(query(test_query), 1):
        print(f"[{i}] Source: {result['source']}")
        print(result["text"])
        print()
