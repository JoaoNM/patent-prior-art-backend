from fill_mask import find_related_keywords
from hf_inferrer import query

trial_text = "The present innovation provides a torque sensor that is small and highly rigid and for which high production efficiency is possible."

print(find_related_keywords(trial_text, 'innovation'))