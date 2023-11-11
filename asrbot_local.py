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
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import audiofile
import librosa

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo user audio."""

    audio_file = await update.message.voice.get_file()

    # load audio into numpy array
    tmp_file = "voice_note.ogg"
    await audio_file.download_to_drive(tmp_file)

    # transcription
    processor = AutoProcessor.from_pretrained("openai/whisper-large-v3")
    model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large-v3")
    target_sr = processor.feature_extractor.sampling_rate

    signal, sampling_rate = audiofile.read("voice_note.ogg")
    if sampling_rate != target_sr:
        signal = librosa.resample(signal, orig_sr=sampling_rate, target_sr=target_sr)

    inputs = processor(signal, sampling_rate=target_sr, return_tensors="pt")
    input_features = inputs.input_features
    generated_ids = model.generate(inputs=input_features)
    output = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    # respond audio
    await update.message.reply_text(output)


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