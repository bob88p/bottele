def format_message(text: str) -> str:
    """Format a message with emoji."""
    if not text:
        return "📭 (فاضي)"
    return f" {text.strip()}"


def is_valid_command(text: str) -> bool:
    """Check if text is a valid bot command."""
    return text.startswith("/") and len(text) > 1