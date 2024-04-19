"""
Using Mistral 7B: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2

Login to download Mistral
```bash
huggingface-cli login
```
"""

import requests
from keys import HUGGING_FACE_KEY
from pprint import pprint
import time


n_words = 10
question = "Who won the world cup in 2010?"

# LOCAL
from transformers import pipeline

pipe = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")

start_time = time.time()
output = pipe(f"{question} (in {n_words} words)")
pprint(output)
print("Time taken (local) :", time.time() - start_time)


# REMOTE
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
start_time = time.time()
output = query({
	"inputs": f"{question} (in {n_words} words)",
})
pprint(output)
print("Time taken (remote):", time.time() - start_time)
