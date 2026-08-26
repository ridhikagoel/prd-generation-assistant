"""Thin client for a local Ollama server — zero-cost, no API key, no billing."""
import json

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"


def chat(model: str, prompt: str, json_mode: bool = False, temperature: float = 0.7) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": temperature},
    }
    if json_mode:
        payload["format"] = "json"

    resp = requests.post(OLLAMA_URL, json=payload, timeout=180)
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def chat_json(model: str, prompt: str, temperature: float = 0.0, retries: int = 2) -> dict:
    last_err = None
    for _ in range(retries + 1):
        raw = chat(model, prompt, json_mode=True, temperature=temperature)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            last_err = e
            prompt = prompt + f"\n\nYour previous response was not valid JSON ({e}). Return ONLY valid JSON, nothing else."
    raise RuntimeError(f"Model never returned valid JSON after {retries + 1} attempts: {last_err}")
