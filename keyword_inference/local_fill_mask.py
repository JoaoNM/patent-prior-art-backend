from transformers import AutoModelForMaskedLM, AutoTokenizer, pipeline

model_local_path = "./bert-for-patents"

model = AutoModelForMaskedLM.from_pretrained(model_local_path)
tokenizer = AutoTokenizer.from_pretrained(model_local_path)

fill_mask_pipeline = pipeline("fill-mask", model=model, tokenizer=tokenizer)


# write a function that replaces a given word with '[MASK]' and returns the result
def find_related_keywords(input_text, word):
    results = [[], [], [], [], []]
    j = 0
    input_text = input_text.replace(word, '[MASK]')
    result = fill_mask_pipeline(input_text)
    for i in result: 
        results[j] = [i['token_str'], i['score']]
        j += 1
    return results

input_text = "The present [MASK] provides a torque sensor that is small and highly rigid and for which high production efficiency is possible."

result = fill_mask_pipeline(input_text)

for i in result:
    print(i['token_str'], i['score'])
    print('\n')