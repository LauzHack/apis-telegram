import requests
from keys import HUGGING_FACE_KEY
import time


API_URL = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3"
headers = {
    "Authorization": f"Bearer {HUGGING_FACE_KEY}",
}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers={"Content-Type": "audio/wav", **headers}, data=data)
    return response.json()

start_time = time.time()
output = query("voice_note_ex.wav")


print(output["text"])
print("Time taken :", time.time() - start_time)