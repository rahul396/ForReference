from elasticsearch import Elasticsearch
from datetime import datetime
import random
from feeder import documents, mappings


class LocalElasticNode:
    def __init__(self):
        self.client = Elasticsearch(hosts='localhost')

    def create_index(self, name, mappings):
        self.client.indices.create(index=name, body=mappings)

    def add_documents(self, index_name, doc_type, documents):
        i = random.randint(1, 10000000000)
        for doc in documents:
            self.client.create(id=i, index=index_name,
                               doc_type=doc_type, body=doc)
            i += 1

    def delete_document(self, name, doc_type):
        query = {
            "query": {
                "match": {"name": name}
            }

        }

        results = self.client.search(body=query,doc_type=doc_type)
        index = results['hits']['hits'][0]['_index']
        iD = results['hits']['hits'][0]['_id']
        if results['hits']['hits'][0]['_type'] == doc_type:
            self.client.delete(index, doc_type, iD)

    def delete_duplicates(self):
        results = self.get_all_documents()
        hits = results['hits']['hits']
        all_names = [h['_source']['name'] for h in hits]
        to_delete_names = []
        f = {}
        # create a dictionary with count of each name
        for k in all_names:
            if not k in f:
                f[k] = 1
            else:
                f[k] += 1
        # Get a list of extra items to delete. e.g if there are 3 A's in a list, get 2 A's out of it
        for k in f:
            while f[k] > 1:
                to_delete_names.append(k)
                f[k] -= 1
        print(to_delete_names)
        for name in to_delete_names:
            print('deleting duplicates by name...')
            self.delete_document(name, 'event')

    def get_all_documents(self):
        query = {
            "query": {
                "match_all": {}
            }
        }
        return self.client.search(body=query)

    def search_by_description(self, description):
        query = {
            "query": {
                "match": {
                    "description": description
                }
            }
        }
        print("Searching...")
        return self.client.search(body=query)

    def search_by_phrase(self, phrase, word_bandwidth):
        query = {
            "query": {
                "match_phrase": {
                    "name": {
                        "query": phrase,
                        "slop": word_bandwidth
                    }
                }
            }
        }
        print("Searching...")
        return self.client.search(body=query)


if __name__ == '__main__':
    localNode = LocalElasticNode()
    # print('adding documents')
    # documents = [
    #     {
    #         'name':'Just a negative test',
    #         'description':'This is just to test what happens if we pass a document of different format'
    #     },
    # ]
    # localNode.add_documents('events','event',documents)
    # results = localNode.search_by_description('heisengbergs principle')
    # results = search_by_phrase(client,'heisenbergs principle',3)
    # results = localNode.get_all_documents()
    # hits = results['hits']['hits']
    # for hit in hits:
    #     print (hit)
    localNode.delete_duplicates()
