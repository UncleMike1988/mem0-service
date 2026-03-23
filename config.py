import os


def get_required_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


OPENAI_API_KEY = get_required_env("OPENAI_API_KEY")
QDRANT_URL = get_required_env("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
MEM0_API_KEY = os.getenv("MEM0_API_KEY", "")
PORT = int(os.getenv("PORT", "8000"))

MEM0_CONFIG = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "url": QDRANT_URL,
            "api_key": QDRANT_API_KEY if QDRANT_API_KEY else None,
        },
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "api_key": OPENAI_API_KEY,
        },
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": OPENAI_API_KEY,
        },
    },
}
