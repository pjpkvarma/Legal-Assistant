from fastapi import APIRouter, Form
import requests

router = APIRouter()

def call_llm(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt, "stream": False},
        timeout=30
    )
    return response.json()["response"].strip()

@router.post("/chat/")
def legal_assistant_chat(message: str = Form(...)):
    prompt = f"You are Legal Assistant, an AI trained to answer legal questions in simple terms. Answer this:\n\n{message}"
    reply = call_llm(prompt)
    return {"response": reply}
