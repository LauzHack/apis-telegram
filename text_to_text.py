import requests
from keys import HUGGING_FACE_KEY
import time


API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"
headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	

start_time = time.time()
#output = query({
#	"inputs": "Меня зовут Вольфганг и я живу в Берлине",
#	"parameters": {"src_lang": "ru_RU", "tgt_lang": "fr_FR"}
#})
output = query({
	"inputs": "Ciao, mi chiamo Matthias e oggi facciamo un hackaton",
	"parameters": {"src_lang": "it_IT", "tgt_lang": "fr_XX"}
})

print(output)
print("Time taken:", time.time() - start_time)