import os
import requests
import numpy as np
import pandas as pd
import json

os.environ['DATABRICKS_API_TOKEN'] = 'dapic07e6257c572690da776699434ce3a6a'
os.environ['DATABRICKS_API_URL'] = 'https://dbc-967c02c1-b6af.cloud.databricks.com/serving-endpoints/dare_amazon_rag_endpoint/invocations'


def create_tf_serving_json(data):
    return {'columns': ["messages"], "data": [[{"messages": data}]]}


def score_model(dataset):
    headers = {'Authorization': f'Bearer {os.environ.get("DATABRICKS_API_TOKEN")}',
               'Content-Type': 'application/json'}
    ds_dict = {"dataframe_split": create_tf_serving_json(dataset)}
    data_json = json.dumps(ds_dict, allow_nan=True)
    response = requests.request(
        method='POST', headers=headers, url=os.environ.get("DATABRICKS_API_URL"), data=data_json)
    if response.status_code != 200:
        raise Exception(
            f'Request failed with status {response.status_code}, {response.text}')
    return response.json()


test_case_1 = {
    "dataframe_split": {
        "columns": [
            "messages"
        ],
        "data": [
            [
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": "What is Apache Spark?"
                        },
                        {
                            "role": "assistant",
                            "content": "Apache Spark is an open-source data processing engine that is widely used in big data analytics."
                        },
                        {
                            "role": "user",
                            "content": "Tell me about why a team would use Spark instead of other open source frameworks"
                        }
                    ]
                }
            ]
        ]
    }
}


test_case_2 = [{
    "role": "user",
    "content": "What is Apache Spark?"
},
    {
    "role": "assistant",
    "content": "Apache Spark is an open-source data processing engine that is widely used in big data analytics."
},
    {
    "role": "user",
    "content": "Tell me about why a team would use Spark instead of other open source frameworks"
}]


test_output = {'predictions': [{'sources': ['dbfs:/Volumes/dare/amazon_rag/wr_test/llm-papers/Databricks-Unified-Analytics-Platform-eBook.pdf', 'dbfs:/Volumes/dare/amazon_rag/wr_test/llm-papers/Databricks-Unified-Analytics-Platform-eBook.pdf', 'dbfs:/Volumes/dare/amazon_rag/wr_test/llm-papers/Databricks-Unified-Analytics-Platform-eBook.pdf', 'dbfs:/Volumes/dare/amazon_rag/wr_test/llm-papers/Databricks-Unified-Analytics-Platform-eBook.pdf'],
                                'result': 'Spark is the de facto standard for big data processing and analytics. It can handle any and all data sources, whether structured, unstructured, or streaming. It is also agnostic to whether data is fed from the cloud or on-premises. Spark is the largest open source community in big data with over 1000 contributors from 250+ orgs. It includes libraries for SQL, streaming, machine learning, ETL, SQL Analytics, Machine Learning, Streaming, and graph. It is trusted by some of the largest enterprises such as Netflix, Yahoo, Facebook, eBay, and Alibaba. Databricks, a company that contributes 75% of the code, 10x more than any other company, has taken performance to another level through Databricks Runtime. Databricks is built on top of Spark and natively built for'}]}

print("SOURCES:")
print(test_output['predictions'][0]['sources'])
print("\nRESULTS:")
print(test_output['predictions'][0]['result'])
