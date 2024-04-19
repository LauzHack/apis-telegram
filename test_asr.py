import requests
from keys import HUGGING_FACE_KEY
import time


API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

start_time = time.time()
output = query("voice_note_ex.ogg")
start_time = time.time()

print(output["text"])
print("Time taken:", time.time() - start_time)