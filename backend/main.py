from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.chatbot import legal_assistant
import requests

# Initialize FastAPI app
app = FastAPI()

# Register chatbot router with a prefix
app.include_router(legal_assistant.router, prefix="/legal-assistant")

# Optional: Enable CORS if frontend runs on a different domain or port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production to specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def call_llm(prompt: str) -> str:
    """
    Sends a prompt to the locally running LLaMA2 model via Ollama
    and retrieves the generated response.

    Args:
        prompt (str): The text prompt to send to the LLM.

    Returns:
        str: The model's textual response.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama2", "prompt": prompt, "stream": False},
            timeout=30
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except requests.exceptions.RequestException as e:
        return f"Error communicating with LLM backend: {e}"

@app.post("/analyze/")
def analyze_legal(text: str = Form(...)):
    """
    Endpoint to analyze legal documents.

    Accepts raw legal text and returns:
    - A summary of the content
    - Extracted key clauses
    - Named entities (e.g., people, dates, organizations)

    Args:
        text (str): Legal document text input by the user.

    Returns:
        dict: Dictionary containing 'summary', 'clauses', and 'entities'.
    """
    prompts = {
        "summary": f"Summarize this legal document:\n\n{text}",
        "clauses": f"Extract key clauses from this legal text:\n\n{text}",
        "entities": f"Extract all named entities (names, dates, money, locations):\n\n{text}"
    }

    results = {key: call_llm(prompt) for key, prompt in prompts.items()}
    return results
