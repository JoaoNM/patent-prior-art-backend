import os
import sys
import pandas as pd
import numpy as np
import time

# Set up imports from other directories
parent_dir = os.path.dirname(os.path.abspath(__file__))
keyword_inf_path = os.path.join(parent_dir, "keyword_inference")
utils_path = os.path.join(parent_dir, "utils")
sys.path.append(keyword_inf_path)
sys.path.append(utils_path)

# Only using HF API for now. It's faster– this is just for demo purposes. 
from keyword_inference import hf_inferrer
from keyword_inference import local_fill_mask
from utils import query_patents, detect_abstract_keywords, compare_patents

def extract_synonym_data(synonym_request_response):
    extracted_synonyms = set()

    try:
        if type(synonym_request_response[0]) == list:
            # It's a 2D list.
            # Make sure to not add duplicate words 
            for i in range(len(synonyms_response)):
                for j in range(len(synonyms_response[i])):
                    extracted_synonyms.add(synonyms_response[i][j]["token_str"])
        else: 
            # It should be a 1D list
            for i in range(len(synonyms_response)):
                extracted_synonyms.add(synonyms_response[i]["token_str"])
    except:
        print("Error extracting synonyms from response. Check the response format.")
        print(synonym_request_response)

        if (type(synonym_request_response) == dict):
            if (synonym_request_response["error"] == 'Model anferico/bert-for-patents is currently loading'):
                print("Model is loading. Waiting 30s to request again...")
                time.sleep(30)

        return []
    
    return list(extracted_synonyms)

# STEP 1: Paste your patent abstract here. 
# STEP 2: Detect keywords in the abstract [DONE]

# (GHOST STEP: Run inference query on the keywords, to find more related keywords (divergence))

# STEP 4: Query BQ to find patents with the detected keywords [DONE]
# STEP 5: Run inference query on patents found compared with the original patent. MASK word should be the same in both cases. (run for every keyword) [HALF-DONE]
# STEP 6: Get comparison score, and return top 10 patents with the highest score.

patent_abstract = input("Paste your base patent abstract here: ")
# remove in production: 
patent_abstract = "The present invention relates to an ovarian-derived hydrogel material, which can be useful for three-dimensional in vitro culturing of cells, cell therapy, fertility preservation, drug delivery, site-specific remodeling and repair of damaged tissue, and/or diagnostic kits."

# Detect keywords in abstract! 

keywords = detect_abstract_keywords.get_keywords_from_gpt(patent_abstract)

# Query BQ to find patents with the detected keywords. Break the query response into a list of abstracts
patents_df = pd.DataFrame()

patents_df['publication_number'] = []
patents_df['title'] = []
patents_df['abstract'] = []
patents_df['url'] = []
patents_df['keyword'] = []
patents_df['similarity_score'] = []

print("Finding similar patents for each keyword...")

# Set true / false to use the HF API or the local model
use_hf_api = False
if (use_hf_api):
    def fetch_synonyms(patent_abstract, keyword):
        return hf_inferrer.find_keyword_synonyms(patent_abstract, keyword)
else:
    def fetch_synonyms(patent_abstract, keyword):
        return local_fill_mask.find_related_keywords(patent_abstract, keyword)

for i in range(len(keywords)):
    print(f"KEYWORD [{i + 1}/{len(keywords)}]: {keywords[i]}")
    df = query_patents.find_similar_patents_to(keywords[i])
    df['keyword'] = keywords[i]
    patents_df = pd.concat([patents_df, df], ignore_index=True)

print("SAMPLE RANDOM 30 ROWS:")
print(patents_df.sample(30))

# Run inference query on both patents. Extract list of keyword synonyms. Then, compare similarity scores.
keyword_index = 0
keyword = keywords[keyword_index]
print("STARTING INFERENCE QUERIES...")
print(f"KEYWORD 1: {keyword}")
original_synonyms = []
while (len(original_synonyms) == 0):
    synonyms_response = fetch_synonyms(patent_abstract, keyword)
    original_synonyms = extract_synonym_data(synonyms_response)

for index, row in patents_df.iterrows():
    synonyms_response = []

    if (keyword_index != np.floor(index / 25)):
        keyword_index += 1
        keyword = keywords[keyword_index]
        # we need to refresh the synonyms list
        original_synonyms = []
        while (len(original_synonyms) == 0):
            synonyms_response = fetch_synonyms(patent_abstract, keyword)
            original_synonyms = extract_synonym_data(synonyms_response)
        
        print("\n\n------------------------------------------------")
        print(f"KEYWORD {keyword_index + 1}: {keyword}")
        print("\n.------------------------------------------------")
        print(original_synonyms)
    
    compare_synonyms = []
    while (len(compare_synonyms) == 0):
        synonyms_response = fetch_synonyms(row['abstract'], keyword)
        compare_synonyms = extract_synonym_data(synonyms_response)

    print(f"Comparing patent {index + 1}/{len(patents_df)}, KEYWORD: {keyword}...")
    print(compare_synonyms)
    similarity_score = compare_patents.get_similarity_score(original_synonyms, compare_synonyms)
    patents_df.at[index, 'similarity_score'] = similarity_score
    print(similarity_score)
    
    # get 

# Ok, all the data is there! sort patents, and now we have the most similar! 

patents_df = patents_df.sort_values(by=['similarity_score'], ascending=False)

print("TOP 100 PATENTS:")
print(patents_df.head(100))


