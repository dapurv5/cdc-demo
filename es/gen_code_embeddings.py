#!/usr/bin/env/python

"""
Writes the code embeddings in an output file in the following format
code: d1,d2, ... d99
"""
import argparse
import numpy as np


def main(args):
  with open(args.input) as input_file:
    with open(args.output, 'wb') as output_file:
      for line in input_file:
        line = line.strip("\n")
        code = line
        #generate the embedding from the code
        embedding = list(np.random.random(size=int(args.dim)))
        embedding = [str(x) for x in embedding]
        output_file.write(code + ":" + ",".join(embedding)+"\n")



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--input', help='path to input file to generate indexable documents from',required=True)
  parser.add_argument('--output', help='path to the output file', required=True)
  parser.add_argument('--dim', help='the dimensionality', required=True)
  args = parser.parse_args()
  main(args)