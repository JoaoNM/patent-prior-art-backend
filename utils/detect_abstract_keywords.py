import query_gpt

message_template = "Can you identify SINGULAR keywords in the following abstract. Please only respond with a list of SINGULAR keywords (no spaces in the keywords. hyphenrs are acceptable). Format this as comma-separated list. DO NOT INCLUDE ANYTHING ELSE. SINGULAR KEYWORDS, NO SPACES (hyphens are ok). COMMA SEPARATED LIST FORMAT. DO NOT INCLUDE the words 'invention', 'innovation' or very close synonyms This is the abstract: "

# additional_comments parameter is included to build in flexibility for future use cases. i.e. avoid words about XYZ. For now, MVP purposes only. 
def get_keywords_from_gpt(abstract, additional_comments=""):
    response = query_gpt.query_gpt(message_template + "\"" + abstract + "\"")
    response = response.replace(".", "")
    response = response.replace(", ", "-")
    response = response.split("-")

    # returns array of keywords
    return response

# test case

# abstract = "The present invention relates to an ovarian-derived hydrogel material, which can be useful for three-dimensional in vitro culturing of cells, cell therapy, fertility preservation, drug delivery, site-specific remodeling and repair of damaged tissue, and/or diagnostic kits."

# print(get_keywords_from_gpt(abstract))