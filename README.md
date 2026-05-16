# SHL Conversational Assessment Recommender

A stateless FastAPI-based conversational agent that recommends SHL assessments from the official SHL product catalog.

## Features

- Conversational SHL assessment recommendation
- Clarifies vague hiring requests before recommending
- Recommends 1–10 catalog-grounded assessments
- Supports refinement using full conversation history
- Supports comparison queries
- Refuses off-topic and prompt-injection requests
- Uses FAISS semantic retrieval over scraped SHL catalog
- Optional Groq LLM layer with fallback
- Strict schema-compatible `/chat` response

## API Endpoints

### Health

```http
GET /health