# Written Responses — Senior AI Engineer Challenge

---

**Question 1 — Production Incident**

The first thing I would do is confirm the issue with data, not assumptions. I’d check logs, recent responses, and metrics to verify that ~20% of responses are indeed returning a null QA score and identify when it started. Since there are no errors being thrown, this points to a silent failure—most likely an issue with how we’re parsing or validating the LLM response.

Next, I’d inspect a few raw LLM outputs for those failed cases. I’d want to see whether the model is returning malformed JSON, missing the QA score field, or deviating from the expected schema. If that’s the case, I’d compare prompts and outputs between working and failing cases to identify patterns.

In parallel, I’d roll back or hotfix if the issue is impacting users significantly. A quick mitigation could be adding stricter output validation and a fallback (e.g., retrying the LLM call or defaulting to a safe value with logging).

Then I’d review recent changes—prompt edits, model version changes, or parsing logic updates—to pinpoint the root cause. Once identified, I’d fix it and add safeguards: stricter schema enforcement, better logging of raw outputs, and possibly a retry mechanism.

Finally, I’d add monitoring for output quality (not just errors) to catch similar issues earlier in the future.

**Question 2 — Ambiguous Requirements**

Given the ambiguity, I’d start by narrowing the problem into something deliverable quickly while keeping future scalability in mind. My first step would be to clarify expectations with the founder—specifically what “search by topic” means in practice and what a good result looks like. But I wouldn’t block on that; I’d move forward with a reasonable assumption.

I’d build a simple semantic search system using embeddings. Each transcript would be embedded and stored in a vector database. On the query side, user inputs like “calls where the agent apologized” would also be embedded, and I’d retrieve the most similar transcripts using vector similarity.

This approach works well because it handles fuzzy, natural language queries without requiring rigid keyword matching. It also scales reasonably for 10,000 transcripts without over-engineering.

For the first version, I’d focus on:

Clean ingestion pipeline (chunking if needed)
Embedding + indexing
Simple search endpoint returning top-k results

If needed, I’d enhance it later with metadata filtering (e.g., tags like “apology” or “pricing”), or even hybrid search (keyword + vector).

The goal is to get a working system quickly, validate it with real queries, and iterate based on actual user behavior rather than assumptions.

