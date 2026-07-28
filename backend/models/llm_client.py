"""Shared LLM client — wraps Groq API (free tier). Every agent imports call_llm from here."""
import os
from dotenv import load_dotenv
from groq import Groq
from backend.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)
_client = None


def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set in .env")
        _client = Groq(api_key=api_key)
    return _client


def call_llm(prompt: str, system: str = "You are a helpful assistant.",
              model: str = "llama-3.3-70b-versatile", temperature: float = 0.7) -> str:
    """Single-turn LLM call. Returns plain text, empty string on failure."""
    try:
        client = get_client()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return ""