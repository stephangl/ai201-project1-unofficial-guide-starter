import os


def load_documents(folder: str) -> list[dict]:
    docs = []
    for fname in sorted(os.listdir(folder)):
        if fname.endswith(".txt"):
            path = os.path.join(folder, fname)
            with open(path, "r", encoding="utf-8") as f:
                docs.append({"source": fname, "text": f.read()})
    return docs


def chunk_by_paragraphs(text: str, max_chars: int = 500, min_chars: int = 100) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        if current and current_len + len(para) + 2 > max_chars:
            chunks.append("\n\n".join(current))
            current = [current[-1], para]
            current_len = len(current[0]) + len(para) + 2
        else:
            current.append(para)
            current_len += len(para) + 2

    if current:
        chunks.append("\n\n".join(current))

    return [c for c in chunks if len(c) >= min_chars]


def build_chunks(folder: str) -> list[dict]:
    docs = load_documents(folder)
    result = []
    for doc in docs:
        for i, chunk in enumerate(chunk_by_paragraphs(doc["text"])):
            result.append({
                "source": doc["source"],
                "chunk_id": f"{doc['source']}_{i}",
                "text": chunk,
            })
    return result


if __name__ == "__main__":
    chunks = build_chunks("documents")
    print(f"Total chunks: {len(chunks)}")
    for chunk in chunks[:3]:
        print(f"\n[{chunk['chunk_id']}] ({len(chunk['text'])} chars)")
        print(chunk["text"])
