"""API key resolution from env, Streamlit secrets, and local file."""
from pathlib import Path
from typing import Optional

from config import API_KEY_FILE, GEMINI_API_KEY


def _read_local_key() -> str:
    key_path = Path(API_KEY_FILE)
    if key_path.exists():
        return key_path.read_text(encoding="utf-8").strip()
    return ""


def resolve_api_key(session_key: Optional[str] = None) -> str:
    """Resolve Gemini API key from session, secrets, env, or local file."""
    if session_key and session_key.strip():
        return session_key.strip()

    try:
        import streamlit as st

        if hasattr(st, "secrets") and st.secrets.get("GEMINI_API_KEY"):
            return str(st.secrets["GEMINI_API_KEY"]).strip()
    except Exception:
        pass

    if GEMINI_API_KEY:
        return GEMINI_API_KEY.strip()

    return _read_local_key()


def save_api_key_locally(api_key: str) -> None:
    Path(API_KEY_FILE).write_text(api_key.strip(), encoding="utf-8")


def is_demo_mode(api_key: str, force_demo: bool = False) -> bool:
    return force_demo or not bool(api_key and api_key.strip())
