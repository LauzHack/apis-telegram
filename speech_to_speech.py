from openai import OpenAI
from keys import OPENAI_KEY
from text_to_text import text_to_text

def speech_to_speech(audio_filename: str, target_lang: str):
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
    response = client.audio.speech.create(
		model="tts-1",
		voice="alloy",
		input=translated_text,
	)
    filename = "speech_to_speech.mp3"
    with open(filename, "wb") as audio_file:
        audio_file.write(response.content)
    print(f"Audio file saved as: {filename}")
    return filename


#audio_filename = "text_to_speech.mp3"
#target_lang = "en_XX"
#speech_to_speech(audio_filename, target_lang)