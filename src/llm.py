import os
from functools import lru_cache
from typing import Optional

import requests


ALLOWED_ROUTES = {
    "team",
    "batting",
    "bowling",
    "venue",
    "h2h",
    "form",
    "records",
    "trend",
    "comparison",
    "validation",
    "prediction",
    "dream11",
    "general",
}


def _get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    return OpenAI(api_key=api_key)


def _get_model() -> str:
    return os.getenv("LLM_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")


def _get_provider() -> str:
    return os.getenv("LLM_PROVIDER", "auto").lower()


def _hf_token() -> Optional[str]:
    return os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")


def _hf_model() -> str:
    return os.getenv("HF_MODEL", _get_model())


@lru_cache(maxsize=1)
def _hf_available() -> bool:
    return bool(_hf_token())


def _hf_generate(prompt: str, temperature: float = 0.0, max_new_tokens: int = 256) -> Optional[str]:
    token = _hf_token()
    if not token:
        return None

    model = _hf_model()
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": temperature,
            "max_new_tokens": max_new_tokens,
            "return_full_text": False,
        },
        "options": {"wait_for_model": True},
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
    except Exception:
        return None

    data = response.json()

    if isinstance(data, list) and data:
        first = data[0]
        if isinstance(first, dict):
            text = first.get("generated_text") or first.get("summary_text")
            if text:
                return str(text).strip()
    elif isinstance(data, dict):
        text = data.get("generated_text") or data.get("summary_text") or data.get("error")
        if text and "error" not in data:
            return str(text).strip()

    return None


@lru_cache(maxsize=1)
def _ollama_available() -> bool:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def _ollama_chat(messages: list[dict], temperature: float = 0.0) -> Optional[str]:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    payload = {
        "model": _get_model(),
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }

    try:
        response = requests.post(f"{base_url}/api/chat", json=payload, timeout=30)
        response.raise_for_status()
    except Exception:
        return None

    data = response.json()
    message = data.get("message", {})
    content = message.get("content")

    if not content:
        return None

    return str(content).strip()


def llm_available() -> bool:
    provider = _get_provider()
    if provider == "huggingface":
        return _hf_available()
    if provider == "ollama":
        return _ollama_available()
    if provider == "openai":
        return _get_client() is not None

    return _hf_available() or _ollama_available() or _get_client() is not None


def classify_route_with_llm(query: str) -> Optional[str]:
    provider = _get_provider()

    prompt = (
        "Classify the IPL query into exactly one label from this set: "
        f"{sorted(ALLOWED_ROUTES)}.\n"
        "Return only the label, nothing else.\n\n"
        f"Query: {query}"
    )

    if provider in {"auto", "huggingface"} and _hf_available():
        content = _hf_generate(prompt, temperature=0, max_new_tokens=8)
        if content is not None:
            label = content.strip().lower()
            label = label.replace('"', "").replace("'", "")
            if label in ALLOWED_ROUTES:
                return label
        if provider == "huggingface":
            return None

    if provider in {"auto", "ollama"} and _ollama_available():
        content = _ollama_chat(
            [
                {
                    "role": "system",
                    "content": "You route IPL dataset questions to the correct node.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        if content is None:
            if provider == "ollama":
                return None
        else:
            label = content.strip().lower()
            label = label.replace('"', "").replace("'", "")
            if label in ALLOWED_ROUTES:
                return label

    client = _get_client()
    if client is None:
        return None

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You route IPL dataset questions to the correct node.",
                },
                {"role": "user", "content": prompt},
            ],
        )
    except Exception:
        return None

    label = response.choices[0].message.content.strip().lower()
    label = label.replace('"', "").replace("'", "")

    if label in ALLOWED_ROUTES:
        return label

    return None


def synthesize_with_llm(prompt: str) -> Optional[str]:
    provider = _get_provider()

    if provider in {"auto", "huggingface"} and _hf_available():
        content = _hf_generate(prompt, temperature=0.2, max_new_tokens=350)
        if content is not None:
            return content
        if provider == "huggingface":
            return None

    if provider in {"auto", "ollama"} and _ollama_available():
        content = _ollama_chat(
            [
                {
                    "role": "system",
                    "content": (
                        "You are an IPL assistant. Use only the provided dataset context. "
                        "Do not invent facts. Be concise but clear."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        if content is not None:
            return content
        if provider == "ollama":
            return None

    client = _get_client()
    if client is None:
        return None

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an IPL assistant. Use only the provided dataset context. "
                        "Do not invent facts. Be concise but clear."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
    except Exception:
        return None

    return response.choices[0].message.content.strip()
