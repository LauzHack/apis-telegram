from openai import OpenAI
from keys import OPENAI_KEY
from text_to_text import text_to_text

def text_to_speech(input: str, target_lang: str, input_lang: str = None):
	print(f"Input text: {input}")
	translated_text = text_to_text(input, target_lang)
	print(f"Translated text: {translated_text}")
	api_key = OPENAI_KEY
	client = OpenAI(api_key=api_key)
	response = client.audio.speech.create(
		model="tts-1",
		voice="alloy",
		input=translated_text,
	)
	filename = "text_to_speech.mp3"
	with open(filename, "wb") as audio_file:
		audio_file.write(response.content)
	print(f"Audio file saved as: {filename}")
	return filename

#input1 = "Ciao, mi chiamo Massimo e oggi facciamo un hackaton!"
#target_lang = "fr_XX"
#text_to_speech(input1, target_lang)