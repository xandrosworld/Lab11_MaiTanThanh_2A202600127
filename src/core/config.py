"""
Lab 11 - Configuration & API Key Setup
"""
from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
GEMINI_KEY_ENV_NAMES = [
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "GOOGLE_GENAI_API_KEY",
    "GOOGLE_API_KEYS",
    "GEMINI_API_KEYS",
]


def load_project_env(env_path: Path | None = None) -> None:
    """Load a local .env file without requiring python-dotenv."""
    target = env_path or ENV_FILE
    if not target.exists():
        return

    for raw_line in target.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _split_key_values(raw_value: str) -> list[str]:
    """Parse a comma or newline separated list of Gemini keys."""
    separators_normalized = raw_value.replace("\r", "\n").replace(",", "\n")
    return [item.strip() for item in separators_normalized.split("\n") if item.strip()]


def get_gemini_api_keys() -> list[str]:
    """Return unique Gemini API keys from env and local .env."""
    load_project_env()

    key_values: list[str] = []
    for env_name in GEMINI_KEY_ENV_NAMES:
        env_value = os.getenv(env_name, "").strip()
        if not env_value:
            continue
        if env_name.endswith("_KEYS"):
            key_values.extend(_split_key_values(env_value))
        else:
            key_values.append(env_value)

    unique_keys: list[str] = []
    for key in key_values:
        if key not in unique_keys:
            unique_keys.append(key)
    return unique_keys


def activate_gemini_key(index: int = 0) -> str | None:
    """Select one Gemini key and expose it through the env names ADK expects."""
    keys = get_gemini_api_keys()
    if not keys:
        return None

    normalized_index = index % len(keys)
    selected = keys[normalized_index]
    os.environ["GOOGLE_API_KEY"] = selected
    os.environ["GOOGLE_GENAI_API_KEY"] = selected
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
    os.environ["GEMINI_ACTIVE_KEY_INDEX"] = str(normalized_index)
    return selected


def get_active_key_index() -> int:
    """Return the current active key index."""
    try:
        return int(os.getenv("GEMINI_ACTIVE_KEY_INDEX", "0"))
    except ValueError:
        return 0


def rotate_gemini_key() -> str | None:
    """Advance to the next Gemini key when the current one is exhausted."""
    keys = get_gemini_api_keys()
    if len(keys) <= 1:
        return None
    next_index = (get_active_key_index() + 1) % len(keys)
    return activate_gemini_key(next_index)


def mask_api_key(api_key: str | None) -> str:
    """Return a short, non-sensitive display form of a key."""
    if not api_key:
        return "none"
    if len(api_key) <= 10:
        return f"{api_key[:3]}...{api_key[-2:]}"
    return f"{api_key[:6]}...{api_key[-4:]}"


def is_gemini_quota_error(exc: Exception) -> bool:
    """Detect quota or rate-limit style errors from Gemini-compatible clients."""
    message = str(exc).lower()
    keywords = [
        "resource_exhausted",
        "quota",
        "429",
        "rate limit",
        "rate_limit",
        "too many requests",
    ]
    return any(keyword in message for keyword in keywords)


def setup_api_key():
    """Load Gemini API keys from env/.env and activate one for the current run."""
    load_project_env()
    selected = activate_gemini_key(get_active_key_index())
    if not selected:
        manual_key = input("Enter Gemini API Key: ").strip()
        os.environ["GOOGLE_API_KEY"] = manual_key
        os.environ["GOOGLE_GENAI_API_KEY"] = manual_key
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
        print("API key loaded.")
        return

    print(
        f"Gemini key loaded: {mask_api_key(selected)} "
        f"(pool size: {len(get_gemini_api_keys())})"
    )


def get_model_name() -> str:
    """Return the Gemini model used across the lab."""
    load_project_env()
    return os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)


# Allowed banking topics (used by topic_filter)
ALLOWED_TOPICS = [
    "banking", "account", "transaction", "transfer",
    "loan", "interest", "savings", "credit",
    "deposit", "withdrawal", "balance", "payment",
    "tai khoan", "giao dich", "tiet kiem", "lai suat",
    "chuyen tien", "the tin dung", "so du", "vay",
    "ngan hang", "atm",
]

# Blocked topics (immediate reject)
BLOCKED_TOPICS = [
    "hack", "exploit", "weapon", "drug", "illegal",
    "violence", "gambling", "bomb", "kill", "steal",
]


load_project_env()
