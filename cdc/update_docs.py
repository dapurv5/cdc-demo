#!/usr/bin/env/python
#
# author: apurvverma@gatech.edu


import argparse
import csv
import sys
import json

from elasticsearch import Elasticsearch

def main(args):
  index_name = 'cdc-demo'
  es = Elasticsearch()
  with open(args.input) as input_file:
    for line in input_file:
      json_doc = json.loads(line)
      res = es.index(index=index_name, doc_type = 'book', id = int(json_doc['pid'], 16), body = json_doc)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--input',help='path to input file to generate indexable documents from',required=True)
  parser.add_argument('--output', help='path to the output file which will contain the json documents', required=True)
  args = parser.parse_args()
  main(args)