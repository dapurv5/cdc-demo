#!/usr/bin/env/python
#
# author: apurvverma@gatech.edu

import argparse
import matplotlib.pyplot as plt
import time
import numpy as np
from elasticsearch import Elasticsearch

diagnostic_codes = []
size_of_query = 3

def plot(X, Y, xlabel, ylabel):
  plt.plot(X, Y)
  plt.ylabel(ylabel)
  plt.xlabel(xlabel)
  plt.show()


def make_query(code_list, dim):
  return {
          "query": {
             "stored_vector_product_query": {
               "query": list(code_list),
               "field_scoring": "embedding",
               "field_retrieval": "codes",
               "dimensionality": str(dim)
             }
           }
         }
  
def main(args):
  index_name = 'psim'
  es = Elasticsearch()
  #Read the input file and store the diagnostic codes
  with open(args.input) as input_file:
    for line in input_file:
      line = line.strip()
      diagnostic_codes.append(line)
  
  latency = []
  dimensionality = []
  
  for dim in range(5, int(args.max_dim), int(args.step_dim)):
    total_time = 0
    cnt = 0
    for i in range(1,5):
      time.sleep(1)
      query = make_query(np.random.choice(diagnostic_codes, size_of_query, replace=False), dim)
      res = es.search(index=index_name, body = query, request_timeout=60)
      time_taken = int(res['took'])
      num_results = res['hits']['total']
      if num_results > 0:
        total_time = time_taken + total_time
        cnt = cnt + 1
    print "dim=", dim, " total_time = ", total_time, " cnt = ", cnt, " avg = ", float(total_time)/float(cnt)
    latency.append(float(total_time)/float(cnt))
    dimensionality.append(dim)
  plot(dimensionality, latency, 'dimensionality', 'latency in milliseconds')
    
    
#python measure_latency.py --input ../codes.txt --max_dim 2000 --step_dim 10
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--input',help='list of diagnostic codes',required=True)
  parser.add_argument('--max_dim', help='the max dimensionality', required=True)
  parser.add_argument('--step_dim', help='step size of the dimension', required=True)
  args = parser.parse_args()
  main(args)