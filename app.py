import os
import sys
import pandas as pd
import numpy as np
import concurrent.futures
import multiprocessing as mp

# Set up imports from other directories
parent_dir = os.path.dirname(os.path.abspath(__file__))
keyword_inf_path = os.path.join(parent_dir, "keyword_inference")
utils_path = os.path.join(parent_dir, "utils")
sys.path.append(keyword_inf_path)
sys.path.append(utils_path)

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Using local model version for keyword inference. HF API maxes out request limits. 
from keyword_inference import local_fill_mask
from utils import query_patents, detect_abstract_keywords, compare_patents

# --------------------------------------------------------------------------------
# HIGH LEVEL OVERVIEW: 

# STEP 1: Paste your patent abstract here. 
# STEP 2: Detect keywords in the abstract [DONE]
# (GHOST STEP: Run inference query on the keywords, to find more related keywords (divergence))
# STEP 4: Query BQ to find patents with the detected keywords [DONE]
# STEP 5: Run inference query on patents found compared with the original patent. MASK word should be the same in both cases. (run for every keyword) [HALF-DONE]
# STEP 6: Get comparison score, and return top 10 patents with the highest score.
# --------------------------------------------------------------------------------

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

        return []
    
    return list(extracted_synonyms)

def fetch_synonyms(patent_abstract, keyword):
    return local_fill_mask.find_related_keywords(patent_abstract, keyword)

if __name__ == '__main__':

    mp.set_start_method('spawn')

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

    # TODO: Parallelize this. Make it more efficient 
    # with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        # synonym_results = list(executor.map(fetch_batch_synonyms, abstracts_batch))

    for i in range(len(keywords)):
        print(f"KEYWORD [{i + 1}/{len(keywords)}]: {keywords[i]}")
        df = query_patents.find_similar_patents_to(keywords[i])
        df['keyword'] = keywords[i]
        patents_df = pd.concat([patents_df, df], ignore_index=True)

    print("SAMPLE RANDOM 30 ROWS:")
    print(patents_df.sample(30))

    # Run inference query on both patents. Extract list of keyword synonyms. Then, compare similarity scores.
    # keyword_index = 0
    # keyword = keywords[keyword_index]
    print("STARTING INFERENCE QUERIES...")
    # print(f"KEYWORD 1: {keyword}")
    # original_synonyms = []
    # while (len(original_synonyms) == 0):
    #     synonyms_response = fetch_synonyms(patent_abstract, keyword)
    #     original_synonyms = extract_synonym_data(synonyms_response)


    # NEW CODE: 
    # (requesting inferences for all patents at once, via parrelelization)
    last_row = patents_df.shape[0]
    for i in range(len(keywords)):
        # For each keyword, grab the original keywords 
        keyword = keywords[i]
        original_synonyms = []
        synonyms_response = fetch_synonyms(patent_abstract, keyword)
        original_synonyms = extract_synonym_data(synonyms_response)

        print("\n\n------------------------------------------------")
        print(f"KEYWORD {i + 1}: {keyword}")
        print("OG SYNONYMS: ", original_synonyms)
        print("\n------------------------------------------------")

        # batching abstracts 25 at a time
        start_index = i * 25
        end_index = start_index + 25
        abstracts_batch = patents_df.loc[start_index:end_index, 'abstract'].tolist()

        # Use ProcessPoolExecutor to parallelize the pipeline calls
        print("Fetching batch of synonyms...")
        with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
            # create functions to pass fixed keyword argument (for 25 patent batch)
            def fetch_batch_synonyms(input_abstract):
                return fetch_synonyms(input_abstract, keyword)
            def batch_compare_synonyms(compare_synonyms):
                return compare_patents.get_similarity_score(original_synonyms, compare_synonyms)
            

            # Run the fetch_batch_synonyms function on each input text in parallel
            synonym_results = list(executor.map(fetch_batch_synonyms, abstracts_batch))
            extracted_synonym_lists = [extract_synonym_data(synonym_result) for synonym_result in synonym_results]

            print("Comparing patent keywords...")
            # Run the batch_compare_synonyms function on each input text in parallel
            similarity_results = list(executor.map(batch_compare_synonyms, extracted_synonym_lists))

        # Add similarity score to dataframe 
        patents_df.loc[start_index:end_index, 'similarity_score'] = similarity_results
        # print dataframe preview from start_index to end_index
        print(patents_df.loc[start_index:end_index, ['publication_number', 'title', 'abstract', 'url', 'keyword', 'similarity_score']])





    # OLD CODE:
    # (individually requesting inferences for each patent)
    # for index, row in patents_df.iterrows():
    #     synonyms_response = []

    #     if (keyword_index != np.floor(index / 25)):
    #         keyword_index += 1
    #         keyword = keywords[keyword_index]
    #         # we need to refresh the synonyms list
    #         original_synonyms = []
    #         while (len(original_synonyms) == 0):
    #             synonyms_response = fetch_synonyms(patent_abstract, keyword)
    #             original_synonyms = extract_synonym_data(synonyms_response)
            
    #         print("\n\n------------------------------------------------")
    #         print(f"KEYWORD {keyword_index + 1}: {keyword}")
    #         print("\n.------------------------------------------------")
    #         print(original_synonyms)
        
    #     compare_synonyms = []
    #     while (len(compare_synonyms) == 0):
    #         synonyms_response = fetch_synonyms(row['abstract'], keyword)
    #         compare_synonyms = extract_synonym_data(synonyms_response)

    #     print(f"Comparing patent {index + 1}/{len(patents_df)}, KEYWORD: {keyword}...")
    #     print(compare_synonyms)
    #     similarity_score = compare_patents.get_similarity_score(original_synonyms, compare_synonyms)
    #     patents_df.at[index, 'similarity_score'] = similarity_score
    #     print(similarity_score)
        
        # get 

    # Ok, all the data is there! sort patents, and now we have the most similar! 

    patents_df = patents_df.sort_values(by=['similarity_score'], ascending=False)

    print("TOP 100 PATENTS:")
    print(patents_df.head(100))


