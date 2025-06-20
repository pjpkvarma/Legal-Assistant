# Legal Analyzer & Legal Assistant Chatbot

A dual-function AI tool to:
- Analyze legal documents (summarize, extract clauses, detect entities)
- Answer legal queries using an intelligent chatbot

## Features

- Paste legal contracts and analyze key content
- Ask legal questions in plain English
- FastAPI backend + Streamlit UI
- Powered by LLaMA2 via Ollama

## Tech Stack
- FastAPI
- Streamlit
- Ollama (LLaMA2 model)

## Setup

```bash
ollama pull llama2
uvicorn backend.main:app --reload
streamlit run frontend/app.py
