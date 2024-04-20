from openai import OpenAI
from keys import OPENAI_KEY
from text_to_text import text_to_text

def speech_to_text(audio_filename: str, target_lang: str, input_lang: str = None):
    print(f"Input audio file: {audio_filename}")
    api_key = OPENAI_KEY
    client = OpenAI(api_key=api_key)

    audio_file= open(audio_filename, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    input_text = transcription.text
    print(f"Input transcription: {input_text}")
    translated_text = text_to_text(input_text, target_lang)
    print(f"Translated text: {translated_text}")
    return translated_text

#input1 = "example_italiano.mp3"
#target_lang = "fr_XX"
#speech_to_text(input1, target_lang)