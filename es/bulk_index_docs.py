#!/usr/bin/env/python
#
# author: apurvverma@gatech.edu

"""
Simple indexer for indexing json documents in elasticsearch

An example of a simple query is

{
  "fields": ["codes", "pid"],
  "query": {
    "term": {
      "codes": "5770"
    },
    "term": {
      "codes": "3091"
    }
  }
}
"""

import argparse
import json

from pyelasticsearch import ElasticSearch
from pyelasticsearch import bulk_chunks

class Indexer(object):
  
  def __init__(self, input):
    self.input = input
    self.es = ElasticSearch()
    self.index_name = "psim"
    self.doc_type = 'book'
    
  def delete_index(self):
    # Delete index if already found one
    try:
      self.es.delete_index(index = self.index_name)
    except Exception:
      pass
  
  def create_index(self):
    self.es.create_index(index=self.index_name, settings = self.get_index_settings())
    
  def get_index_settings(self):
    settings = {
                        "mappings": {
                           "book": {
                             "_all" : {"enabled" : "false"},       
                             "properties": {
                                "codes": {"type": "string",
                                         "term_vector": "yes",
                                         "store": "true"},
                                "pid" : {"type" : "string"},
                                "embedding": {"type": "float",
                                              "store": "true"}
                             }     
                           }
                        }
               }
    return settings
  
  def documents(self):
    with open(self.input) as input_file:
      for line in input_file:
        json_doc = json.loads(line)
        yield self.es.index_op(json_doc, doc_type=self.doc_type)
    
  def index(self):
    self.delete_index()
    self.create_index()
    for chunk in bulk_chunks(self.documents(), docs_per_chunk=1000):
      self.es.bulk(chunk, index = self.index_name, doc_type = self.doc_type)
    self.es.refresh(self.index_name)


def main(args):
  indexer = Indexer(args.input)
  indexer.index()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--input',help='path to input file to generate indexable documents from',required=True)
  args = parser.parse_args()
  main(args)
