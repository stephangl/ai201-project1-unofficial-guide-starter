# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This system covers Search Engine Optimization (SEO) — specifically the intersection of traditional SEO, Answer Engine Optimization (AEO), and Generative Engine Optimization (GEO) as they stand in 2025–2026. It draws on 10 expert sources covering technical SEO, keyword research, schema markup, Core Web Vitals, and how AI-powered search tools like ChatGPT and Perplexity are changing content visibility.

This knowledge is valuable because SEO is not a single topic — it spans technical implementation (Core Web Vitals, structured data), content strategy (E-E-A-T, AEO), and emerging AI search behaviors (GEO). Official documentation from Google covers individual pieces but does not synthesize across them. Practitioner guides fill that gap but are scattered across dozens of publications. This system brings them together in one queryable knowledge base.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Airops | Blog article | https://www.airops.com/blog/aeo-answer-engine-optimization — `documents/airops_aeo.txt` |
| 2 | CXL | Blog article | https://cxl.com/blog/answer-engine-optimization-aeo-the-comprehensive-guide/ — `documents/aeo-guide-2026.txt` |
| 3 | Google | Developer documentation | https://developers.google.com/search/docs/fundamentals/seo-starter-guide — `documents/google-seo-starter-guide.txt` |
| 4 | Ahrefs | Guide / Tutorial | https://ahrefs.com/seo/keyword-research — `documents/ahrefs-keyword-research-guide.txt` |
| 5 | Webflow | Blog article | https://webflow.com/blog/schema-markup — `documents/webflow-schema-markup-guide.txt` |
| 6 | Elementera | Blog article | https://www.elementera.com/blog/schema-markup-for-aeo-seo-geo-ai-seo — `documents/elementera-schema-markup-aeo-guide.txt` |
| 7 | AlmCorp | Blog article | https://almcorp.com/blog/core-web-vitals-2026-technical-seo-guide/ — `documents/alm-core-web-vitals-2026.txt` |
| 8 | Creative Corner | Blog article | https://www.creativecorner.studio/blog/seo-vs-aeo-vs-geo — `documents/creative-corner-seo-aeo-geo-2026.txt` |
| 9 | Writesonic | Blog article | https://writesonic.com/blog/geo-vs-seo — `documents/writesonic-geo-vs-seo-guide.txt` |
| 10 | Google | Developer documentation | https://developers.google.com/search/docs/fundamentals/get-started-developers — `documents/google-search-developer-guide.txt` |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
~500 characters (paragraph-aware, so actual size varies by paragraph length)

**Overlap:**
One paragraph — the last paragraph of each chunk is carried into the start of the next chunk as the overlap unit.

**Why these choices fit your documents:**
Documents are pre-saved as plain `.txt` files, so ingestion is a direct file read with no HTML stripping needed. An initial character-based split at 500 chars with 50-char overlap was tested first, but 3 out of 5 sampled chunks started mid-sentence or mid-word, making them unable to stand alone as retrievable units. The approach was switched to paragraph-aware splitting: the text is split on `\n\n` first to get natural paragraph units, then paragraphs are grouped until the total reaches ~500 chars. This respects the author's intended structure and guarantees every chunk starts and ends at a paragraph boundary. Chunks under 100 chars (section headers with no body text) are filtered out before storage since they contain no answerable content.

**Final chunk count:**
628 chunks across 10 documents.

---

## Sample Chunks

Five labeled chunks drawn from five different source documents:

**Chunk 1** — `aeo-guide-2026.txt` (470 chars)
> Answer Engine Optimization (AEO): The Comprehensive Guide for 2026 — By Stefan Maritz | Source: CXL Blog. Search is changing. Fast. And the traffic you were once drawing in is likely nowhere near what it used to be. Not because your rankings tanked, but because users are getting their answers without ever clicking through to your site.

**Chunk 2** — `ahrefs-keyword-research-guide.txt` (393 chars)
> How to Do Keyword Research for SEO (Start to Finish) — Source: Ahrefs SEO Guide, by Tim Soulo. 90% of pages get no organic traffic from Google. All of that hard work, all of that effort... for zero visitors.

**Chunk 3** — `airops_aeo.txt` (495 chars)
> SUMMARY (TL;DR) — Answer engine optimization (AEO) is structuring content so AI platforms like ChatGPT, Perplexity, and Google AI Overview can extract, trust, and cite it as a direct answer.

**Chunk 4** — `alm-core-web-vitals-2026.txt` (218 chars)
> Core Web Vitals 2026: Technical SEO That Actually Moves the Needle — Source: ALM Corp Blog, Published: December 24, 2025.

**Chunk 5** — `creative-corner-seo-aeo-geo-2026.txt` (216 chars)
> SEO vs AEO vs GEO: An Honest 2026 Comparison — Source: Creative Corner Studio Blog, Author: Miroslav Ivanov, Published: May 18, 2026.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
`all-MiniLM-L6-v2` via `sentence-transformers`. Chosen because it runs fully locally with no API key or rate limits, produces 384-dimensional embeddings fast enough for interactive use, and performs well on general English text.

**Production tradeoff reflection:**
- **Accuracy:** MiniLM is a general-purpose model; a domain-specific model like `text-embedding-3-large` would handle SEO jargon (E-E-A-T, LCP, schema types) more precisely but costs more per query.
- **Context length:** 500-char chunks fit blog paragraphs well, but a model supporting longer inputs (e.g., `text-embedding-ada-002` at 8191 tokens) could embed full sections and preserve more context per chunk.
- **Latency vs accuracy:** MiniLM runs locally with no network overhead; switching to an API-based embedding model adds latency on every query — an important tradeoff when users expect near-instant answers.

---

## Retrieval Test Results

**Query 1:** "What percentage of Google searches were zero-click in 2025?"

| Rank | Distance | Source |
|------|----------|--------|
| 1 | 0.6274 | creative-corner-seo-aeo-geo-2026.txt |
| 2 | 0.7406 | aeo-guide-2026.txt |
| 3 | 0.7616 | aeo-guide-2026.txt |

*Why the chunks are relevant:* Chunk [1] contains the exact statistic ("Zero-click searches climbed from 56% to 69% between May 2024 and May 2025") and comes from a source that cites Search Engine Land directly. Chunks [2] and [3] both cover the same zero-click trend from the CXL guide, reinforcing the answer with supporting context about user behavior and click-through rates.

---

**Query 2:** "What schema markup type should you use for FAQ content?"

| Rank | Distance | Source |
|------|----------|--------|
| 1 | 0.6187 | elementera-schema-markup-aeo-guide.txt |
| 2 | 0.6909 | airops_aeo.txt |
| 3 | 0.7296 | airops_aeo.txt |

*Why the chunks are relevant:* Chunk [1] explicitly names FAQPage and explains the mechanism — it "gives every AI system crawling your page a prepackaged question-and-answer pair." Chunks [2] and [3] from Airops independently confirm FAQPage as the highest-impact schema type for AEO, providing corroboration from a second source.

---

**Query 3:** "What are the three Core Web Vitals metrics?"

| Rank | Distance | Source |
|------|----------|--------|
| 1 | 0.6123 | alm-core-web-vitals-2026.txt |
| 2 | 0.7231 | alm-core-web-vitals-2026.txt |
| 3 | 0.7460 | alm-core-web-vitals-2026.txt |

All three chunks come from the dedicated Core Web Vitals article, which is the expected source. Chunk [1] names all three metrics (LCP, INP, CLS) directly and contains the answer.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The system prompt enforces grounding with a hard instruction, not a suggestion:

> *"Your ONLY source of information is the numbered context blocks provided in the user message. Do NOT use any knowledge from your training data. If the answer is not present in the provided context, respond exactly with: 'The provided sources do not contain enough information to answer this question.'"*

The retrieved chunks are passed to the model as numbered blocks `[1]` through `[5]` in the user message, each labeled with its source filename. The model is instructed to reference them by number. Temperature is set to 0.2 to reduce creative deviation from the context.

**How source attribution is surfaced in the response:**
Source attribution is programmatically guaranteed — it is never left to the LLM to add. After the Groq response is returned, `build_sources_markdown()` deduplicates the source filenames from the retrieved chunk metadata and appends them as a separate **Sources** block in the UI. This block renders on every response unconditionally, even when the model returns the fallback refusal phrase.

---

## Query Interface

**Input field:** Single text box labeled "Your question" — accepts any natural language question. Pressing Enter or clicking the "Ask" button submits the query.

**Output fields:** Two separate components rendered below the input:
1. **Answer** — Markdown-rendered response from Groq `llama-3.3-70b-versatile`, grounded in the retrieved chunks. References context blocks by number (e.g. [1], [2]).
2. **Sources** — Deduplicated list of source filenames, programmatically built from chunk metadata and rendered unconditionally on every response.

---

**Example response 1 — in-scope query with source attribution:**

> **Question:** What are the three Core Web Vitals metrics?
>
> **Answer:** The three core metrics are LCP, INP, and CLS, as mentioned in [1].
>
> **Sources**
> - alm-core-web-vitals-2026.txt

---

**Example response 2 — in-scope query with multiple sources:**

> **Question:** What schema markup type should you use for FAQ content?
>
> **Answer:** FAQPage schema markup should be used for FAQ content, as it structures question-and-answer pairs in the format AI systems use [1], [3], [5].
>
> **Sources**
> - elementera-schema-markup-aeo-guide.txt
> - airops_aeo.txt

---

**Example response 3 — out-of-scope query showing refusal:**

> **Question:** What is the best programming language to learn in 2026?
>
> **Answer:** The provided sources do not contain enough information to answer this question.
>
> **Sources**
> - alm-core-web-vitals-2026.txt
> - aeo-guide-2026.txt
> - creative-corner-seo-aeo-geo-2026.txt
> - elementera-schema-markup-aeo-guide.txt

The system returned the exact fallback phrase defined in the system prompt. The sources panel still renders — showing which documents were retrieved — even though none contained relevant content for the query.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What percentage of Google searches were zero-click in 2025? | 69% (sourced from the CXL AEO guide) | "69% of Google searches were zero-click in 2025 [1], [4]." | Relevant | Accurate |
| 2 | What is the difference between AEO and GEO? | AEO targets AI answer engines returning direct answers; GEO optimizes for visibility within AI-generated responses in tools like ChatGPT and Perplexity | "AEO is on-site structural work under your control; GEO is off-site brand signal work on platforms like Reddit and YouTube, mostly out of your control. AEO is a one-time investment; GEO is ongoing." | Relevant | Accurate |
| 3 | What schema markup type should you use for FAQ content? | FAQPage structured data, which wraps Q&A pairs in a machine-readable format AI systems use directly | "FAQPage schema markup should be used for FAQ content, as it structures question-and-answer pairs in the format AI systems use." | Relevant | Accurate |
| 4 | What are the three Core Web Vitals metrics? | LCP (Largest Contentful Paint), INP (Interaction to Next Paint), and CLS (Cumulative Layout Shift) | "The three core metrics are LCP, INP, and CLS." | Relevant | Accurate(However, It does not include the full name) |
| 5 | What does Google's SEO Starter Guide say about structured data and search appearance? | Valid structured data makes pages eligible for rich results (review stars, carousels) in Google Search | "The provided sources do not contain enough information to answer this question." | Refuse to answer | Innacruate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
"What does Google's SEO Starter Guide say about structured data and search appearance?"

**What the system returned:**
"The provided sources do not contain enough information to answer this question."

**Root cause (tied to a specific pipeline stage):**
The failure happened at the retrieval stage. The query phrase "What does Google's SEO Starter Guide say" caused the embedding model to surface chunks that mention Google in the context of schema and structured data — primarily from `elementera-schema-markup-aeo-guide.txt` and `webflow-schema-markup-guide.txt` — rather than chunks from `google-seo-starter-guide.txt` itself. The actual Google Starter Guide document never appeared in the top-5 results (best distance was 0.76, the weakest across all 5 queries). Because none of the retrieved chunks came from the right source, the model correctly refused to answer rather than hallucinate — but the underlying problem is that the query phrasing matched the topic of structured data broadly rather than the specific document.

**What you would change to fix it:**
Rephrase the query to focus on the content rather than the source name — for example, "How does structured data affect rich results in Google Search?" would retrieve chunks from `google-seo-starter-guide.txt` more reliably. Alternatively, increasing k from 5 to 7 would give the retriever more slots and a higher chance of pulling in the correct source document alongside the schema-focused results.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The AI Tool Plan in planning.md named specific function signatures for each milestone (`load_documents()`, `chunk_by_paragraphs()`, `embed_and_store()`, `query()`), which made it possible to give Claude a precise prompt rather than a vague one. Instead of saying "write me a RAG pipeline," each milestone prompt could reference the exact function name, input type, and output type already written in the spec. This produced code that matched the architecture.

**One way your implementation diverged from the spec, and why:**
The chunking approach diverged significantly from the original spec. The plan called for character-based splitting at 500 chars with 50-char overlap. During testing, 3 out of 5 sampled chunks started mid-sentence or mid-word, meaning they could not stand alone as retrievable units. The implementation was switched to paragraph-aware splitting — splitting on `\n\n` first, then grouping paragraphs up to ~500 chars — which the original spec did not anticipate. The architecture diagram in planning.md was updated to reflect this change, but the initial spec did not foresee that structured blog content would require boundary-respecting chunking rather than a fixed-character sliding window.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1 — Chunking implementation and refinement**

- *What I gave the AI:* The Chunking Strategy section from planning.md (500 chars, 50-char overlap, pure Python) and the Documents table, and asked it to implement `ingest.py` with `load_documents()` and `chunk_by_paragraphs()`.
- *What it produced:* A character-based sliding-window chunker that split text every 500 characters regardless of sentence or paragraph boundaries.
- *What I changed or overrode:* After testing, I directed the AI to evaluate whether each chunk could stand alone as a retrievable unit. 3 out of 5 sampled chunks started mid-sentence. I overrode the character-based approach entirely and directed the AI to switch to paragraph-aware splitting on `\n\n`, carrying the last paragraph as overlap. I also added a 100-char minimum filter to drop header-only chunks the spec had not anticipated.

**Instance 2 — Generation interface**

- *What I gave the AI:* The Milestone 5 AI Tool Plan from planning.md (Gradio UI, Groq, RAG prompt, all 5 evaluation questions), and the `retrieve.py` output from Milestone 4, and asked it to implement `app.py`.
- *What it produced:* A Gradio `Blocks` app with a text input, answer output, and sources output, wired to a Groq call using `llama3-8b-8192` with a system prompt enforcing grounding.
- *What I changed or overrode:* I overrode the model from `llama3-8b-8192` to `llama-3.3-70b-versatile` as recommended for production quality. I also directed the AI to separate the sources into a dedicated Gradio component (rather than appending them inside the answer text) so that attribution would render unconditionally on every response, including refusals.
