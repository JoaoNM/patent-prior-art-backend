from transformers import AutoModelForMaskedLM, AutoTokenizer, pipeline
import concurrent.futures
import multiprocessing as mp

model_local_path = "./bert-for-patents"

model = AutoModelForMaskedLM.from_pretrained(model_local_path)
tokenizer = AutoTokenizer.from_pretrained(model_local_path)

fill_mask_pipeline = pipeline("fill-mask", model=model, tokenizer=tokenizer)


# write a function that replaces a given word with '[MASK]' and returns the result
def find_related_keywords(input_text, word):
    input_text = input_text.replace(word, '[MASK]')
    result = fill_mask_pipeline(input_text)
    
    return result

if __name__ == '__main__':

    mp.set_start_method('spawn')

    input_texts = [
        "The present innovation provides a torque sensor that is small and highly rigid and for which high production efficiency is possible.",
        "The present innovation provides a torque sensor that is small and highly rigid and for which high production efficiency is possible.",
        "The present innovation provides a torque sensor that is small and highly rigid and for which high production efficiency is possible.",
        "The present innovation provides a torque sensor that is small and highly rigid and for which high production efficiency is possible.",
        "The present innovation provides a torque sensor that is small and highly rigid and for which high production efficiency is possible.",
        "The present innovation provides a torque sensor that is small and highly rigid and for which high production efficiency is possible.",
        "The present innovation provides a torque sensor that is small and highly rigid and for which high production efficiency is possible.",
        "The present innovation provides a torque sensor that is small and highly rigid and for which high production efficiency is possible.",
    ]

    mask_words = [
        "innovation",
        "torque",
        "sensor",
        "production",
        "efficiency",
        "rigid",
        "possible",
        "highly",
    ]

    # Use ProcessPoolExecutor to parallelize the pipeline calls
    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        # Run the pipeline on each input text in parallel
        results = list(executor.map(find_related_keywords, input_texts, mask_words))

    print(results)


# single_input_text = "The present innovation provides a torque sensor that is small and highly rigid and for which high production efficiency is possible."

# result = find_related_keywords(single_input_text, "innovation")

# print(result)