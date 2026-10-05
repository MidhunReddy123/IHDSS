# IHDSS: Intelligent Healthcare Diagnosis Support System (MVP)

Multi-agent clinical decision support running fully locally: Ollama (qwen3:4b + nomic-embed-text), LangGraph, Chroma, SQLite, Streamlit.
**Synthetic data only. Research/education use; not a medical device.**

## Pipeline (LangGraph)
intake (LLM symptom extraction) -> pattern (lab/vital flags, red flags, drug interactions) -> retrieval (Chroma RAG over guideline summaries)
-> differential (LLM, cites doc ids) -> critic (citation check, confidence capping, ICD-10, red-flag escalation) -> report.
Clinicians accept/reject each suggestion in the UI; decisions and every run are stored in SQLite (feedback and audit tables).

## Run
```
python -m venv .venv && .venv\Scripts\pip install -r requirements.txt
ollama pull qwen3:4b && ollama pull nomic-embed-text
.venv\Scripts\python -m ihdss.setup_data
.venv\Scripts\streamlit run ihdss/ui.py
set PYTHONPATH=. && .venv\Scripts\python evals\run_eval.py
.venv\Scripts\python -m pytest
```

## Limits
Six synthetic patients and seven hand-written guideline summaries. Eval is tiny and says nothing about real-world accuracy.
Runs about 90 s per patient on this machine.
