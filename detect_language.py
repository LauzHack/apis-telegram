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
        return map_code(label_max)
    else:
        top_languages = []
        for i in range(NUMBER_OF_TOP_LANGUAGES):
            current_score = sorted_array[i]['score']
            current_label = sorted_array[i]['label']
            if current_score > TOP_CERTAINTY_RATE_LIMIT:
                top_languages.append(current_label)
        #print("Top languages:", top_languages)
        return map_code(top_languages)

def map_code(shortCode : str):
    match shortCode:
        case "ar":
            return "ar_AR"
        case "cs":
            return "cs_CZ"
        case "de":
            return "de_DE"
        case "en":
            return "en_XX"
        case "es":
            return "es_XX"
        case "et":
            return "et_EE"
        case "fi":
            return "fi_FI"
        case "fr":
            return "fr_XX"
        case "gu":
            return "gu_IN"
        case "hi":
            return "hi_IN"
        case "it":
            return "it_IT"
        case "ja":
            return "ja_XX"
        case "kk":
            return "kk_KZ"
        case "ko":
            return "ko_KR"
        case "lt":
            return "lt_LT"
        case "lv":
            return "lv_LV"
        case "my":
            return "my_MM"
        case "ne":
            return "ne_NP"
        case "nl":
            return "nl_XX"
        case "ro":
            return "ro_RO"
        case "ru":
            return "ru_RU"
        case "si":
            return "si_LK"
        case "tr":
            return "tr_TR"
        case "vi":
            return "vi_VN"
        case "zh":
            return "zh_CN"
        case "af":
            return "af_ZA"
        case "az":
            return "az_AZ"
        case "bn":
            return "bn_IN"
        case "fa":
            return "fa_IR"
        case "he":
            return "he_IL"
        case "hr":
            return "hr_HR"
        case "id":
            return "id_ID"
        case "ka":
            return "ka_GE"
        case "km":
            return "km_KH"
        case "mk":
            return "mk_MK"
        case "ml":
            return "ml_IN"
        case "mn":
            return "mn_MN"
        case "mr":
            return "mr_IN"
        case "pl":
            return "pl_PL"
        case "ps":
            return "ps_AF"
        case "pt":
            return "pt_XX"
        case "sv":
            return "sv_SE"
        case "sw":
            return "sw_KE"
        case "ta":
            return "ta_IN"
        case "te":
            return "te_IN"
        case "th":
            return "th_TH"
        case "tl":
            return "tl_XX"
        case "uk":
            return "uk_UA"
        case "ur":
            return "ur_PK"
        case "xh":
            return "xh_ZA"
        case "gl":
            return "gl_ES"
        case "sl":
            return "sl_SI"
        case _:
            return "en_XX"


# Testing
input1 = "Ciao, mi chiamo Matthias"
input2 = "Hi I am Groot"
#print(detect_language(input1))