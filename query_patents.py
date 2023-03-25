# Set BigQuery application credentials 
from google.cloud import bigquery

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./google_credentials.json"

project_id = 'plasma-hope-381607'
bq_client = bigquery.Client(project=project_id)

def find_similar_patents_to(keyword):
    # Returns Top 10 patents with the keyword
    query = r"""
    SELECT publication_number, abstract, url
    FROM `patents-public-data.google_patents_research.publications` 
    WHERE abstract LIKE '%{}%'
    LIMIT 50
    """.format(keyword)

    df = bq_client.query(query).to_dataframe()

    print("success!")
    print(df.head(50))

    return df

# test case: 
find_similar_patents_to("machine learning")