"""
Using https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503

"""

import requests
from keys import HUGGING_FACE_KEY
import time
import base64


n_words = 10   # negative number means no limit
question = "Who won the world cup in 2010?"


import requests

API_URL = "https://router.huggingface.co/nebius/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {HUGGING_FACE_KEY}",
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

start_time = time.time()

### --- Image-Text to Text
image_url = "https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg"
# # -- or using local image
# image_path = "tmp_photo.jpg"
# with open(image_path, "rb") as f:
#     base64_image = base64.b64encode(f.read()).decode("utf-8")
# image_url = f"data:image/jpeg;base64,{base64_image}"
response = query({
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe this image in one sentence."
                },
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                }
            ]
        }
    ],
    "model": "mistralai/Mistral-Small-3.1-24B-Instruct-2503"
})

# ### --- Text to Text
# if n_words > 0:
# 	question += f" (in {n_words} words or less)"
# response = query({
# 	"messages": [
# 		{
# 			"role": "user",
# 			"content": [
# 				{
# 					"type": "text",
# 					"text": question
# 				}
# 			]
# 		}
# 	],
# 	"model": "mistralai/Mistral-Small-3.1-24B-Instruct-2503"
# })

print(response["choices"][0]["message"]["content"])
print("Time taken :", time.time() - start_time)