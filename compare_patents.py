# Here we are going to compare 2 patents, based on the keywords given

# for the demo, we're not gonna use a model to evaluate similarity. We're going to use that trusty metric of word overlap! 

def get_similarity_score(keywords_patent_a, keywords_patent_b):
    # get the number of keywords that are the same
    num_same_keywords = len(set(keywords_patent_a).intersection(keywords_patent_b))
    # get the total number of keywords
    total_keywords = len(keywords_patent_a) + len(keywords_patent_b)
    # get the similarity score
    similarity_score = num_same_keywords / total_keywords
    return similarity_score