from bot_logic import classify_message, get_message, parse_admin_ids, truncate_text


def test_get_message_accepts_message():
    assert get_message({"message": {"text": "درود"}}) == {"text": "درود"}


def test_get_message_accepts_edited_message():
    assert get_message({"edited_message": {"text": "edited"}}) == {"text": "edited"}


def test_get_message_ignores_callback_without_message():
    assert get_message({"callback_query": {"id": "1"}}) is None


def test_classify_text_and_media():
    assert classify_message({"text": "hello"}) == "text"
    assert classify_message({"photo": [{"file_id": "abc"}]}) == "photo"
    assert classify_message({}) == "unknown"


def test_admin_allowlist_ignores_invalid_entries():
    assert parse_admin_ids("123, nope, 456, -7, 123") == {123, 456}


def test_truncate_text_respects_limit():
    assert truncate_text("abcdef", 4) == "abc…"
    assert truncate_text("  ok  ", 10) == "ok"
