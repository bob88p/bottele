from src.utils import format_message, is_valid_command


def test_format_message_normal():
    assert format_message("hello") == "📢 hello"


def test_format_message_with_spaces():
    assert format_message("  hello  ") == "📢 hello"


def test_format_message_empty():
    assert format_message("") == "📭 (فاضي)"


def test_is_valid_command_true():
    assert is_valid_command("/start") is True


def test_is_valid_command_false():
    assert is_valid_command("hello") is False
    assert is_valid_command("/") is False