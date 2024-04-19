"""

Using Mistral 7B: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2

"""

import requests
from keys import HUGGING_FACE_KEY
from pprint import pprint


API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

n_words = 10
question = "Who won the world cup in 2010?"

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": f"{question} (in {n_words} words)",
})

pprint(output)
