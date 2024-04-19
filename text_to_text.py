import requests
from keys import HUGGING_FACE_KEY
import time
from detect_language import detect_language


API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"
headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def text_to_text(input: str):
    input_language = detect_language(input)
    #print(input_language)
    output = query({
        "inputs": input,
        "parameters": {"src_lang": input_language, "tgt_lang": "fr_XX"}
    })
    return output[0]['translation_text']


# testing
input1 = "Ciao, mi chiamo Matthias e oggi facciamo un hackaton"
input2 = "Меня зовут Вольфганг и я живу в Берлине"
print(text_to_text(input2))

