#!/usr/bin/env/python
#
# author: apurvverma@gatech.edu

"""
Adds the embedding and the magnitude to the json doc
"""

import argparse
import csv
import json
import time
import numpy as np


def main(args):
  code_map = {}
  counter = 0
  with open(args.codes) as codes_file:
    for code in codes_file:
      code = code.strip("\n")
      if code not in code_map:
        code_map[code] = counter
        counter += 1

  embedding_map = {} #map from code index to the embedding array
  dim = -1
  with open(args.embeddings) as embeddings_file:
    for line in embeddings_file:
      line = line.strip("\n")
      code_index = code_map[line.split(":")[0]]
      code_embedding = line.split(":")[1].split(",")
      code_embedding = np.array([float(x) for x in code_embedding])
      dim = len(code_embedding)
      embedding_map[code_index] = code_embedding
  print len(embedding_map)
  
  with open(args.input) as input_file:
    with open(args.output, 'wb') as output_file:
      for line in input_file:
        line = line.strip("\n")
        json_doc = json.loads(line)
        sentence = json_doc["codes"].split(" ")
        sentence = [str(x) for x in sentence]
        
        #compute the average, which corresponds to document-vector
        avg = np.zeros(dim)
        count_codes = 0
        for code in sentence:
          if code == '':
            continue
          code_index = code_map[code]
          count_codes += 1
          avg = avg + embedding_map[code_index]

        if count_codes != 0:
          avg = avg/count_codes
        json_doc["embedding"] = list(avg)
        
        #compute the magnitude of the document vector
        magn = np.sum(avg**2)
        magn = magn ** 0.5
        json_doc["magnitude"] = magn
        output_file.write(json.dumps(json_doc)+"\n")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--input',help='path to input file to generate indexable documents from',required=True)
  parser.add_argument('--codes', help='codes file',required=True)
  parser.add_argument('--embeddings', help='embeddings file', required=True)
  parser.add_argument('--output', help='products file', required=True)
  args = parser.parse_args()
  start_time = time.time()
  main(args)
  end_time = time.time()
  print "Minutes elapsed", (end_time-start_time)/60