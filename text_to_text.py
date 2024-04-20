import requests
from keys import HUGGING_FACE_KEY
import time
from detect_language import detect_language


API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"
headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def text_to_text(input: str, target_lang: str, input_lang: str = None):
    input_language = detect_language(input)
    if isinstance(input_language, list):
          input_language = input_lang
    #print(f"Text input: {input}")
    output = query({
        "inputs": input,
        "parameters": {"src_lang": input_language, "tgt_lang": target_lang}
    })
    print(output)
    translated_text = output[0]['translation_text']
    #print(f"Translated text: {translated_text}")
    return translated_text


# testing
#input1 = "Ciao, mi chiamo Matthias e oggi facciamo un hackaton"
#input2 = "Меня зовут Вольфганг и я живу в Берлине"
#target_lang = "fr_XX"
#text_to_text(input1, target_lang)

