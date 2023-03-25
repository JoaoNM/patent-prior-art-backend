import os
import sys

# Set up imports from other directories
parent_dir = os.path.dirname(os.path.abspath(__file__))
keyword_inf_path = os.path.join(parent_dir, "keyword_inference")
utils_path = os.path.join(parent_dir, "utils")
sys.path.append(keyword_inf_path)
sys.path.append(utils_path)

# Only using HF API for now. It's faster– this is just for demo purposes. 
# from hf_inferrer import query
# from compare_patents import get_similarity_score
from utils import query_patents, detect_abstract_keywords, compare_patents

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

# Query BQ to find patents with the detected keywords. Break the query response into a list of abstract
abstracts = {}

for i in range(len(keywords)):
    df = query_patents.find_similar_patents_to(keywords[i])
    abstracts[keywords[i]] = df["abstract"].tolist()

print(abstracts)




# print(keywords[0])


# print(df.head())

