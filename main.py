import logging
logger = logging.getLogger(_name_)
import os
import re
import uuid
import json
import logging
import warnings
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone, timedelta
warnings.filterwarnings("ignore", category=UserWarning)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(name)

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ADMIN_USERNAME = "mahi115eth"
EARNINGS_PER_SUBMISSION = 5  # ETB
MIN_WITHDRAWAL_ETB = 150  # minimum balance required to withdraw
EAT = timezone(timedelta(hours=3))  # Ethiopia time (UTC+3)

DATA_FILE = os.path.join(os.path.dirname(file), "task_data.json")

DEFAULT_TASK_MESSAGE = (
    "📄 የሁሉ የቤት ስራ መመሪያ፦\n\n"
    "ወደ AI ዳታ መሰብሰቢያ መድረካችን በሰላም መጡ! ስራውን በትክክል ለማጠናቀቅ እባክዎ የሚከተሉትን መመሪያዎች ይከተሉ፦\n\n"
    "1. በግልጽ ማንበብ፦ የሚሰጡትን ጽሑፎች ወይም ቃላት በተፈጥሯዊ ድምጽ ያንብቡ።\n"
    "2. የድምጽ ጥራት ማረጋገጥ፦ በሚቀዱበት ጊዜ በዙሪያው ምንም አይነት የረብሻ ወይም የሙዚቃ ድምጽ አለመኖሩን ያረጋግጡ። ድምጽ ላይ ያለ ግልጽ መሆን አለበት።\n"
    "3. ስራውን ማጠናቀቅ፦ ቀደምን ሲያጠናቅቁ በታች ያለውን \"Submit Work\" የሚለውን ተጭነው ይላኩ።\n"
