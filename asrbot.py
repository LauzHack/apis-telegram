"""
Bot to transcribe audio messages using Hugging Face's whisper-large-v3 model.

```python
python asrbot.py
```

Press Ctrl-C on the command line to stop the bot.
"""

import logging

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from keys import TELEGRAM_KEY

import requests
from keys import HUGGING_FACE_KEY


headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def query_asr(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(
        "https://api-inference.huggingface.co/models/openai/whisper-large-v3", 
        headers=headers, 
        data=data
    )
    return response.json()

async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo user audio."""

    audio_file = await update.message.voice.get_file()

    # load audio into numpy array
    tmp_file = "voice_note.ogg"
    await audio_file.download_to_drive(tmp_file)

    # transcription
    output = query_asr(tmp_file)

    # respond audio
    await update.message.reply_text(output["text"])


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_KEY).build()

    # voice input
    application.add_handler(
        MessageHandler(filters.VOICE & ~filters.COMMAND, voice, block=True)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()