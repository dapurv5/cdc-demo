#!/usr/bin/env/python

"""
Takes in the codes and the embeddings file and produces
products of every pair of codes
"""
import argparse
import numpy as np
import time

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
  with open(args.embeddings) as embeddings_file:
    for line in embeddings_file:
      line = line.strip("\n")
      code_index = code_map[line.split(":")[0]]
      code_embedding = line.split(":")[1].split(",")
      code_embedding = np.array([float(x) for x in code_embedding])
      embedding_map[code_index] = code_embedding
  print len(embedding_map)

  codes = code_map.keys()
  codes = sorted(codes)
  with open(args.output, 'wb') as output_file:
    for code1 in codes:
      for code2 in codes:
        product = np.dot(embedding_map[code_map[code1]], embedding_map[code_map[code2]])
        line = str(code_map[code1]) + "," + str(code_map[code2]) + "," + str(product)
        output_file.write(line + "\n")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--codes', help='codes file',required=True)
  parser.add_argument('--embeddings', help='embeddings file', required=True)
  parser.add_argument('--output', help='products file', required=True)
  args = parser.parse_args()
  start_time = time.time()
  main(args)
  end_time = time.time()
  print "Minutes elapsed", (end_time-start_time)/60
