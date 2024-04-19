import requests
from keys import HUGGING_FACE_KEY
import time

API_URL = "https://api-inference.huggingface.co/models/papluca/xlm-roberta-base-language-detection"
SUCCESS_CERTAINTY_RATE_LIMIT = 0.95
TOP_CERTAINTY_RATE_LIMIT = 0.05
NUMBER_OF_TOP_LANGUAGES = 4

headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def detect_language(input: str):
    output = query({
        "inputs": input,
    })
     # Trier le tableau par score dans l'ordre décroissant
    sorted_array = sorted(output[0], key=lambda x: x['score'], reverse=True)

    # Vérifier si le score le plus élevé est supérieur à SUCCESS_CERTAINTY_RATE_LIMIT
    score_max = sorted_array[0]['score']
    if score_max > SUCCESS_CERTAINTY_RATE_LIMIT:
        label_max = sorted_array[0]['label']
        #print("Best language:", {'label': label_max, 'score': score_max})
        return label_max
    else:
        top_languages = []
        for i in range(NUMBER_OF_TOP_LANGUAGES):
            current_score = sorted_array[i]['score']
            current_label = sorted_array[i]['label']
            if current_score > TOP_CERTAINTY_RATE_LIMIT:
                top_languages.append(current_label)
        #print("Top languages:", top_languages)
        return top_languages

# Testing
input1 = "Ciao, mi chiamo Matthias"
input2 = "Hi I am Groot"
#print(detect_language(input1))


     