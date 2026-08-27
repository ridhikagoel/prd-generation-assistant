"""LLM clients for the PRD pipeline.

Two backends, both zero marginal cost:

- ``ollama``  — a local Ollama server (default). No API key, no account.
- ``claude``  — shells out to the ``claude`` CLI, which runs on the machine's existing
  Claude subscription (no ``ANTHROPIC_API_KEY``, no per-call billing). Use this when you
  want a stronger model than a 3B local one and you already pay for Claude.

Both expose the same ``chat`` / ``chat_json`` surface so the pipeline doesn't care which
one is in use.
"""
import json
import re
import shutil
import subprocess

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

# Default model per backend, used when --model isn't passed.
DEFAULT_MODEL = {
    "ollama": "llama3.2",
    "claude": "claude-sonnet-4-5",
}

_FENCE_RE = re.compile(r"^\s*```(?:json|markdown|md)?\s*\n(.*?)\n```\s*$", re.DOTALL)


def _strip_code_fence(text: str) -> str:
    """The claude CLI often wraps JSON (and sometimes markdown) in a ``` fence. Ollama in
    json mode doesn't. Strip a single wrapping fence if present; leave everything else alone."""
    m = _FENCE_RE.match(text.strip())
    return m.group(1) if m else text


def _chat_ollama(model: str, prompt: str, json_mode: bool, temperature: float) -> str:
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


def _chat_claude(model: str, prompt: str, json_mode: bool, temperature: float) -> str:
    """Run the prompt through the ``claude`` CLI in non-interactive print mode.

    Temperature isn't exposed by the CLI, so it's ignored here — a real tradeoff noted in
    the README: the claude backend can't be dialed to temperature=0 for the JSON judgment
    calls the way the ollama backend is. In practice the JSON calls are constrained enough
    (fixed schema, one-line reasoning fields) that this hasn't mattered.
    """
    if shutil.which("claude") is None:
        raise RuntimeError(
            "claude CLI not found on PATH — install it or use --backend ollama"
        )
    if json_mode:
        prompt = prompt + "\n\nReturn ONLY valid JSON. No prose, no code fence."

    proc = subprocess.run(
        ["claude", "-p", "--model", model],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"claude CLI failed (exit {proc.returncode}): {proc.stderr.strip()}")
    return _strip_code_fence(proc.stdout)


def chat(
    model: str,
    prompt: str,
    json_mode: bool = False,
    temperature: float = 0.7,
    backend: str = "ollama",
) -> str:
    if backend == "ollama":
        return _chat_ollama(model, prompt, json_mode, temperature)
    if backend == "claude":
        return _chat_claude(model, prompt, json_mode, temperature)
    raise ValueError(f"unknown backend: {backend!r}")


def chat_json(
    model: str,
    prompt: str,
    temperature: float = 0.0,
    retries: int = 2,
    backend: str = "ollama",
) -> dict:
    last_err = None
    for _ in range(retries + 1):
        raw = chat(model, prompt, json_mode=True, temperature=temperature, backend=backend)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            last_err = e
            prompt = prompt + f"\n\nYour previous response was not valid JSON ({e}). Return ONLY valid JSON, nothing else."
    raise RuntimeError(f"Model never returned valid JSON after {retries + 1} attempts: {last_err}")
