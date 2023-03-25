from transformers import AutoModelForMaskedLM, AutoTokenizer, pipeline

model_name = "anferico/bert-for-patents"

model = AutoModelForMaskedLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

save_path = "./bert-for-patents"

model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)