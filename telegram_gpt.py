"""
Bot to transcribe audio messages using Hugging Face's whisper-large-v3 model.

```python
python telegram_gpt.py
```


To set commands (after running /setcommands from BotFather):
```
clear - Clear chat history.
```

Press Ctrl-C on the command line to stop the bot.
"""

import logging

from telegram import Update
import requests
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler
from keys import TELEGRAM_KEY, HUGGING_FACE_KEY, OPENAI_KEY
from pprint import pprint
from openai import OpenAI


MAX_CHAT_HISTORY = 10
N_WORDS = 50
VERBOSE = True


global USER_MESSAGES    # user message history

USER_MESSAGES = dict()    # dict of chat/group IDs and their messages



headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

# prepare LLM
client = OpenAI(
    api_key=OPENAI_KEY,
    # # LauzHack
    # organization="org-bcv27ooZj8JyXgpgj5sed8rH",
)

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


def query_llm(input_text, user_id):

    # add to message history
    if user_id in USER_MESSAGES:
        USER_MESSAGES[user_id].append({"role": "user", "content": input_text})
    else:
        USER_MESSAGES[user_id] = [{"role": "user", "content": input_text}]

    # prompt LLM
    # -- OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=USER_MESSAGES[user_id]
    )
    text_response = response.choices[0].message.content
    
    # update message history
    USER_MESSAGES[user_id].append({"role": "assistant", "content": text_response})

    if VERBOSE:
        pprint(USER_MESSAGES[user_id])

    # clear chat history (if too long)
    if len(USER_MESSAGES[user_id]) > 2 * MAX_CHAT_HISTORY:
        # remove bot response
        USER_MESSAGES[user_id].pop(0)
        # remove question
        USER_MESSAGES[user_id].pop(0)

    return text_response


async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """STEP 1) Speech to text."""
    audio_file = await update.message.voice.get_file()

    # load audio into numpy array
    tmp_file = "voice_note.ogg"
    await audio_file.download_to_drive(tmp_file)

    # transcription
    output = query_asr(tmp_file)
    try:
        output = output["text"]
    except:
        output = "Sorry, I could not understand the audio message. Please try again."
        await update.message.reply_text(output)
        return

    """STEP 2) Prompt LLM."""
    # add to message history
    user_id = update.message.from_user.id
    if user_id in USER_MESSAGES:
        USER_MESSAGES[user_id].append({"role": "user", "content": f"{output} (in {N_WORDS} words or less)"})
    else:
        USER_MESSAGES[user_id] = [{"role": "user", "content": f"{output} (in {N_WORDS} words or less)"}]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=USER_MESSAGES[user_id]
    )
    text_response = response.choices[0].message.content

    # respond text through Telegram
    await update.message.reply_text(text_response)

    # add to message history
    USER_MESSAGES[user_id].append({"role": "assistant", "content": text_response})

    if VERBOSE:
        pprint(USER_MESSAGES[user_id])

    """Clear chat history."""
    if len(USER_MESSAGES[user_id]) > 2 * MAX_CHAT_HISTORY:
        # remove bot response
        USER_MESSAGES[user_id].pop(0)
        # remove question
        USER_MESSAGES[user_id].pop(0)


async def text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # prompt LLM
    input_text = update.message.text
    user_id = update.message.from_user.id
    text_response = query_llm(input_text, user_id)

    # respond text through Telegram
    await update.message.reply_text(text_response)


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear chat history."""
    user_id = update.message.from_user.id
    USER_MESSAGES[user_id] = []
    await update.message.reply_text("Chat history cleared.")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_KEY).build()

    # voice input
    application.add_handler(
        MessageHandler(filters.VOICE & ~filters.COMMAND, voice, block=True)
    )

    # text input
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_input, block=True))

    # commands
    application.add_handler(CommandHandler("clear", clear, block=False))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()