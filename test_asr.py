import requests
from keys import HUGGING_FACE_KEY

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("voice_note.ogg")
print(output["text"])