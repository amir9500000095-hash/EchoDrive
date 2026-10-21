"""Pure helpers shared by the Telegram Worker and local unit tests."""
from __future__ import annotations
from typing import Any

MEDIA_FIELDS = ("photo", "video", "audio", "voice", "document", "sticker", "animation", "video_note")


def get_message(update: dict[str, Any]) -> dict[str, Any] | None:
    message = update.get("message") or update.get("edited_message")
    return message if isinstance(message, dict) else None


def classify_message(message: dict[str, Any]) -> str:
    if message.get("text"):
        return "text"
    for field in MEDIA_FIELDS:
        if message.get(field):
            return field
    return "unknown"


def parse_admin_ids(raw: str | None) -> set[int]:
    """Parse a comma-separated allowlist; malformed values are ignored."""
    result: set[int] = set()
    for part in (raw or "").split(","):
        part = part.strip()
        if part.isdigit():
            result.add(int(part))
    return result


def truncate_text(value: str, limit: int = 1200) -> str:
    value = value.strip()
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 1)].rstrip() + "…"
