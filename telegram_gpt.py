"""
Bot to transcribe audio messages using Hugging Face's whisper-large-v3 model.

```python
python telegram_gpt.py
```


To set commands (after running /setcommands from BotFather):
```
clear - Clear chat history.
n_words - How many words for response.
```

Press Ctrl-C on the command line to stop the bot.
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler, CallbackQueryHandler
from keys import TELEGRAM_KEY, HUGGING_FACE_KEY, OPENAI_KEY
from pprint import pprint
from openai import OpenAI
import torch


MAX_CHAT_HISTORY = 10
VERBOSE = True
LOCAL_ASR = False
CUDA_AVAILABLE = torch.cuda.is_available()


global USER_MESSAGES    # user message history
global N_WORDS    # number of words for response

USER_MESSAGES = dict()    # dict of chat/group IDs and their messages
N_WORDS = dict()


headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

# prepare LLM
client = OpenAI(api_key=OPENAI_KEY)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# prepare ASR
if LOCAL_ASR:
    from transformers import pipeline
    import audiofile
    import librosa

    if CUDA_AVAILABLE:
        asr_pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3", device=0)
    else:
        asr_pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
    asr_rate = 16000

# querying ASR
def query_asr(filename):

    if LOCAL_ASR:

        signal, sampling_rate = audiofile.read(filename)
        if sampling_rate != asr_rate:
            signal = librosa.resample(signal, orig_sr=sampling_rate, target_sr=asr_rate)
        output = asr_pipe(signal, generate_kwargs={"language": "english"})
        return output

    else:
        # Hugging Face endpoint
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(
            "https://api-inference.huggingface.co/models/openai/whisper-large-v3", 
            headers=headers, 
            data=data
        )
        return response.json()

# querying LLM
def query_llm(input_text, user_id):

    if user_id not in N_WORDS:
        N_WORDS[user_id] = -1

    if N_WORDS[user_id] > 0:
        input_text += f" (in {N_WORDS[user_id]} words or less)"

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
    text_response = query_llm(output, update.message.from_user.id)

    # respond text through Telegram
    await update.message.reply_text(text_response)


async def text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # prompt LLM
    input_text = update.message.text
    user_id = update.message.from_user.id
    text_response = query_llm(input_text, user_id)

    # respond text through Telegram
    await update.message.reply_text(text_response)


async def n_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """How many words for response."""
    # button for user to accept or reject the suggestion
    keyboard = [
        [
            InlineKeyboardButton("10", callback_data="10"),  # callback_data has to be string
            InlineKeyboardButton("50", callback_data="50"),
        ],
        [
            InlineKeyboardButton("100", callback_data="100"),
            InlineKeyboardButton("None", callback_data="-1"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # get number of words
    await update.message.reply_text("Upper limit for response?", reply_markup=reply_markup)   


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    
    # set number of words
    query = update.callback_query
    user_id = query.from_user.id

    # update number of words
    N_WORDS[user_id] = int(query.data)

    if VERBOSE:
        print(f"Number of words for response: {N_WORDS[user_id]}")
    
    if user_id in USER_MESSAGES:
        # request LLM output again
        # -- remove last two messages
        del USER_MESSAGES[user_id][-1]
        input_text = USER_MESSAGES[user_id][-1]["content"]
        del USER_MESSAGES[user_id][-1]
        text_response = query_llm(input_text, user_id)

        # respond text through Telegram
        await query.message.reply_text(text_response)


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear chat history."""
    user_id = update.message.from_user.id
    del USER_MESSAGES[user_id]
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
    application.add_handler(CommandHandler("n_words", n_words))
    application.add_handler(CommandHandler("clear", clear, block=False))
    application.add_handler(CallbackQueryHandler(button))


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()