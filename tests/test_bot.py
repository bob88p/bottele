import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.bot import start_command, help_command, echo_message, main


# ==================== Command Tests ====================

@pytest.mark.asyncio
async def test_start_command():
    update = MagicMock()
    update.effective_user.first_name = "Ahmed"
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    await start_command(update, context)

    update.message.reply_text.assert_called_once_with("👋 أهلاً Ahmed!")


@pytest.mark.asyncio
async def test_help_command():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    await help_command(update, context)

    update.message.reply_text.assert_called_once_with("🆘 اكتب أي حاجة وهرد عليك!")


@pytest.mark.asyncio
async def test_echo_message():
    update = MagicMock()
    update.message.text = "Hello Bot"
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    await echo_message(update, context)

    update.message.reply_text.assert_called_once_with("📩 قولت: Hello Bot")


# ==================== Main Function Tests ====================

def test_main_missing_bot_token():
    """Should raise ValueError when BOT_TOKEN is missing."""
    with patch("src.bot.BOT_TOKEN", None):
        with pytest.raises(ValueError, match="BOT_TOKEN not found"):
            main()


def test_main_success(mocker):
    """Should build app, add handlers, and run webhook."""
    # Mock Application builder chain
    mock_app = MagicMock()
    mock_builder = MagicMock()
    mock_builder.token.return_value = mock_builder
    mock_builder.build.return_value = mock_app

    mocker.patch("src.bot.Application.builder", return_value=mock_builder)
    mocker.patch("src.bot.logger")

    # Mock environment variables
    with patch("src.bot.BOT_TOKEN", "test_token_123"), \
         patch("src.bot.WEBHOOK_URL", "https://mybot.azurecontainerapps.io"), \
         patch("src.bot.PORT", 80):

        main()

    # Verify token was set
    mock_builder.token.assert_called_once_with("test_token_123")
    mock_builder.build.assert_called_once()

    # ✅ التعديل هنا: تغيير 2 إلى 3 لأننا أضفنا echo_message handler
    assert mock_app.add_handler.call_count == 3

    # Verify run_webhook was called with correct arguments
    mock_app.run_webhook.assert_called_once()
    call_kwargs = mock_app.run_webhook.call_args.kwargs
    assert call_kwargs["listen"] == "0.0.0.0"
    assert call_kwargs["port"] == 80