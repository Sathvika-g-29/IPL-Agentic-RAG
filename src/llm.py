import os
from functools import lru_cache
from typing import Optional

import requests
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()
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


def _get_provider() -> str:
    return os.getenv("LLM_PROVIDER", "gemini").lower()


# =====================================================
# GEMINI
# =====================================================

@lru_cache(maxsize=1)
def _gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    try:
        genai.configure(api_key=api_key)

        model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        return genai.GenerativeModel(model_name)

    except Exception:
        return None


def _gemini_generate(
    system: str,
    prompt: str,
    temperature: float = 0.0,
) -> Optional[str]:

    model = _gemini_model()

    if model is None:
        return None

    try:

        full_prompt = f"""
SYSTEM:
{system}

USER:
{prompt}
"""

        response = model.generate_content(
            full_prompt,
            generation_config={
                "temperature": temperature
            }
        )

        if hasattr(response, "text"):
            return response.text.strip()

    except Exception:
        return None

    return None


# =====================================================
# OPENAI
# =====================================================

def _get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)

    except Exception:
        return None


def _openai_generate(
    system: str,
    prompt: str,
    temperature: float = 0.0,
) -> Optional[str]:

    client = _get_openai_client()

    if client is None:
        return None

    try:

        response = client.chat.completions.create(
            model=os.getenv(
                "OPENAI_MODEL",
                "gpt-4.1-mini"
            ),
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return None


# =====================================================
# OLLAMA
# =====================================================

@lru_cache(maxsize=1)
def _ollama_available():

    base_url = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    try:
        response = requests.get(
            f"{base_url}/api/tags",
            timeout=2
        )

        return response.status_code == 200

    except Exception:
        return False


def _ollama_generate(
    system: str,
    prompt: str,
    temperature: float = 0.0,
) -> Optional[str]:

    if not _ollama_available():
        return None

    base_url = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    payload = {
        "model": os.getenv(
            "OLLAMA_MODEL",
            "qwen2.5:3b"
        ),
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "options": {
            "temperature": temperature
        }
    }

    try:

        response = requests.post(
            f"{base_url}/api/chat",
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"].strip()

    except Exception:
        return None


# =====================================================
# COMMON
# =====================================================

def llm_available() -> bool:

    provider = _get_provider()

    if provider == "gemini":
        return _gemini_model() is not None

    if provider == "openai":
        return _get_openai_client() is not None

    if provider == "ollama":
        return _ollama_available()

    return False


def _generate(
    system: str,
    prompt: str,
    temperature: float = 0.0,
) -> Optional[str]:

    provider = _get_provider()

    if provider == "gemini":
        return _gemini_generate(
            system,
            prompt,
            temperature
        )

    if provider == "openai":
        return _openai_generate(
            system,
            prompt,
            temperature
        )

    if provider == "ollama":
        return _ollama_generate(
            system,
            prompt,
            temperature
        )

    return None


# =====================================================
# ROUTE CLASSIFICATION
# =====================================================

def classify_route_with_llm(
    query: str
) -> Optional[str]:
    prompt = f"""
You are a routing classifier.

Allowed labels:

team
batting
bowling
venue
h2h
form
records
trend
comparison
validation
prediction
dream11
general

Return ONLY ONE WORD.

Query:
{query}
"""
    response = _generate(
    system="You are an IPL routing assistant.",
    prompt=prompt,
    temperature=0,
)
    print("RAW RESPONSE:", response)
    if not response:
        return None
    response = response.lower().strip()
    for route in ALLOWED_ROUTES:
        if route in response:
            return route
    return None


# =====================================================
# ANSWER SYNTHESIS
# =====================================================

def synthesize_with_llm(
    prompt: str
) -> Optional[str]:

    return _generate(
        system=(
            "You are an IPL assistant. "
            "Use only the provided context. "
            "Do not invent facts. "
            "Be concise and accurate."
        ),
        prompt=prompt,
        temperature=0.2,
    )