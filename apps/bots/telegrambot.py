import logging
import datetime

from telegram import Update
from telegram.ext import CallbackContext

from apps.bots import models
from utils.decorators import get_member
from .state import state

logger = logging.getLogger(__name__)


@get_member
def start(update: Update, context: CallbackContext, tg_user: models.TelegramProfile):
    """Send a message asynchronously when the command /start is issued."""
    print(context.user_data)
    context.user_data["start"] = (
        datetime.datetime.now()
        if not context.user_data.get("start")
        else context.user_data["start"]
    )
    try:
        update.message.reply_text("Assalomu alaykum, bot ishladi")
    except Exception as e:
        logger.error(f"Error in start command: {e}")
    print(context.user_data)

    return state.START_POINT


@get_member
def message(update: Update, context: CallbackContext, tg_user: models.TelegramProfile):
    update.message.reply_text("Hello")
