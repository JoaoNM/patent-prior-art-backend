import json
import requests
import auth

API_TOKEN = auth.hf_key

API_URL = "https://api-inference.huggingface.co/models/anferico/bert-for-patents"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# write a function that takes a string, and replaces a given word with '[MASK]' and returns the result
def replace_mask_word(input_text, word):
    return input_text.replace(word, '[MASK]')

def find_keyword_synonyms(payload, mask_word):
    print("Fetching synonyms for keyword (via HF API): ", mask_word)
    payload = replace_mask_word(payload, mask_word)
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

# test query 

# data = find_keyword_synonyms("The present innovation provides a torque sensor that is small and highly rigid and for which high production efficiency is possible.", "innovation")

# print(data)