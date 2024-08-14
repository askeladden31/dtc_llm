from elasticsearch import Elasticsearch
from mage_ai.data_preparation.variable_manager import get_global_variable


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test




@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here

    
    connection_string = 'http://elasticsearch:9200'
    es_client = Elasticsearch(connection_string)

    query = "When is the next cohort?"

    #index_name = "documents_20240814_1049"
    index_name = get_global_variable('captivating_flux', 'index_name')
    print("Index:", index_name)

    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                }
            }
        }
    }

    response = es_client.search(index=index_name, body=search_query)
    
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append({'id': hit['_source']['document_id'], 'score': hit['_score']})
    
    return result_docs


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'