import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.bot import start_command, help_command, echo_message


@pytest.mark.asyncio
async def test_start_command():
    update = MagicMock()
    update.effective_user.first_name = "Ahmed"
    update.message.reply_text = AsyncMock()

    await start_command(update, None)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args[0][0]
    assert "Ahmed" in call_args
    assert "أهلاً" in call_args


@pytest.mark.asyncio
async def test_help_command():
    update = MagicMock()
    update.message.reply_text = AsyncMock()

    await help_command(update, None)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args[0][0]
    assert "المساعدة" in call_args


@pytest.mark.asyncio
async def test_echo_message():
    update = MagicMock()
    update.message.text = "Hello Bot"
    update.message.reply_text = AsyncMock()

    await echo_message(update, None)

    update.message.reply_text.assert_called_once_with("📩 قولت: Hello Bot")
    