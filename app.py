import os
import sys

# Set up imports from other directors 
parent_dir = os.path.dirname(os.path.abspath(__file__))
keyword_inf_path = os.path.join(parent_dir, "keyword_inference")
sys.path.append(keyword_inf_path)

# from local_fill_mask import find_related_keywords

# Only using HF API for now. It's faster– this is just for demo purposes. 
from hf_inferrer import query
from compare_patents import find_similar_patents_to

# STEP 1: Paste your patent abstract here.
# STEP 2: Detect keywords in the abstract 

# (GHOST STEP: Run inference query on the keywords, to find more related keywords (divergence))

# STEP 4: Query BQ to find patents with the detected keywords
# STEP 5: Run inference query on patents found compared with the original patent. MASK word should be the same in both cases. (run for every keyword)
# STEP 6: Get comparison score, and return top 10 patents with the highest score.




