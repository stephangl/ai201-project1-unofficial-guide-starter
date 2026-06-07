import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

from retrieve import query

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are a retrieval-augmented assistant for an SEO knowledge base.

Your ONLY source of information is the numbered context blocks provided in the user message.
Do NOT use any knowledge from your training data.
If the answer is not present in the provided context, respond exactly with:
"The provided sources do not contain enough information to answer this question."

Keep answers concise and factual. You may reference context blocks by their number (e.g. [1], [2])."""


def build_context_block(chunks: list[dict]) -> str:
    lines = []
    for i, chunk in enumerate(chunks, 1):
        lines.append(f"[{i}] (source: {chunk['source']})\n{chunk['text']}")
    return "\n\n".join(lines)


def build_sources_markdown(chunks: list[dict]) -> str:
    seen = []
    for chunk in chunks:
        if chunk["source"] not in seen:
            seen.append(chunk["source"])
    lines = ["**Sources**"] + [f"- {src}" for src in seen]
    return "\n".join(lines)


def answer(question: str) -> tuple[str, str]:
    if not question.strip():
        return "Please enter a question.", ""

    chunks = query(question, k=5)
    context = build_context_block(chunks)

    user_message = f"Context:\n{context}\n\nQuestion: {question}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    answer_text = response.choices[0].message.content
    sources_text = build_sources_markdown(chunks)

    return answer_text, sources_text


with gr.Blocks(title="SEO Unofficial Guide") as app:
    gr.Markdown("## SEO Unofficial Guide\nAsk anything about technical SEO, AEO, GEO, schema markup, Core Web Vitals, and keyword research.")

    question_box = gr.Textbox(
        label="Your question",
        placeholder="e.g. What are the three Core Web Vitals metrics?",
        lines=2,
    )
    submit_btn = gr.Button("Ask", variant="primary")

    answer_box = gr.Markdown(label="Answer")
    sources_box = gr.Markdown(label="Sources")

    submit_btn.click(
        fn=answer,
        inputs=question_box,
        outputs=[answer_box, sources_box],
    )
    question_box.submit(
        fn=answer,
        inputs=question_box,
        outputs=[answer_box, sources_box],
    )

if __name__ == "__main__":
    app.launch()
