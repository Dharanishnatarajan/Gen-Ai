# Day 3 Lab 3: Review Loop Moderation Desk

A content moderation workflow built with LangGraph, Flask, and a browser UI. Messages are scored with heuristic rules, enriched with optional LLM analysis, and then auto-approved, auto-denied, or sent to a human review lane.

---

## Architecture Overview

```
[Ingest] → [Auto-Moderate] → [Route]
                                 ├── score < 0.30 → [Finalize: auto-approve]
                                 ├── score >= 0.70 → [Finalize: auto-deny]
                                 └── 0.30 ≤ score < 0.70 → [Human Review Gate]
                                                                  ↓ (pause)
                                                          Human approves/denies via UI
                                                                  ↓ (resume)
                                                          [Finalize: human decision]
```

---

## Files

| File              | Purpose                                              |
|-------------------|------------------------------------------------------|
| `app.py`          | LangGraph nodes + Flask API (single file, all logic) |
| `index.html`      | Dark-theme interactive frontend (single file)        |
| `requirements.txt`| Python dependencies                                  |
| `.env.example`    | Environment variable template                        |
| `README.md`       | This file                                            |

---

## How to Run

1. Clone / copy all 5 files into a directory.

2. Create a virtual environment (Python 3.10+):
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Groq API key (free at https://console.groq.com):
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

5. (Optional) For local LLM fallback, install Ollama + Mistral:
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull mistral
   ```

6. Run the server:
   ```bash
   python app.py
   ```

7. Open your browser: http://localhost:5000

---

## Thresholds

| Score Range  | Decision       |
|--------------|----------------|
| < 0.25       | Auto-approve   |
| 0.25 - 0.64  | Human review   |
| >= 0.65      | Auto-deny      |

---

## API Endpoints

| Method | Endpoint              | Description                        |
|--------|-----------------------|------------------------------------|
| POST   | /api/moderate         | Submit content for moderation      |
| GET    | /api/queue            | List pending human-review items    |
| POST   | /api/review/<id>      | Submit human approve/deny decision |
| GET    | /api/completed        | List all finalized decisions       |
| GET    | /api/stats            | Dashboard aggregate stats          |

---

## Design Notes — How LangGraph HITL Pause/Resume Works

1. PAUSE: The backend workflow is constructed using `langgraph.graph.StateGraph`. We configure `MemorySaver()` as a checkpointer and specifically compile the graph with `interrupt_before=["human_review"]`. When the `auto_moderate` node conditionally routes the state to the `human_review` node, the graph execution stream is natively suspended, and the checkpointer freezes the thread state. 

2. RESUME: When a human submits a decision via `POST /api/review/<review_id>`, the backend targets the frozen thread using the checkpointer via its `thread_id`. The human input is injected natively using `graph.update_state()`, and the workflow stream is immediately resumed via `graph.stream()`. The workflow proceeds to the `finalize` node organically.

3. AUDIT TRAIL: Every node appends a timestamped event to `state.audit_log`.
   This gives a full chain-of-custody record visible in the UI's audit modal.

4. LLM ENRICHMENT: After heuristic scoring, `llm_analyze()` calls Groq's
   llama-3.1-8b-instant (free tier) to provide a natural-language explanation.
   If Groq is unavailable, it falls back to local Ollama + Mistral. If both
   are down, a plain-text fallback message is stored — the workflow never
   blocks on LLM availability.

5. THREAD SAFETY: A threading.Lock() guards both `review_queue` and
   `completed_items` for safe concurrent access under Flask's dev server.
   For production, replace with Redis + Celery or a proper DB.

---

## Observability

- Each node prints: `[ISO-timestamp] [node_name] summary`
- All events are stored in `state.audit_log` (viewable per-item in the UI)
- The `/api/stats` endpoint provides aggregate counts for the dashboard

---

## LLM Notes

- Primary: Groq `llama-3.1-8b-instant`
- Fallback: Ollama `mistral`
- Rule-based scoring still works even without either LLM path
- No OpenAI, no paid services required
