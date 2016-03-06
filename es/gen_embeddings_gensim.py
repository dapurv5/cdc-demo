#!/usr/bin/env/python

"""
Writes the code embeddings in an output file in the following format
code: d1,d2, ... d99
"""
import argparse
import json
import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def main(args):
  with open(args.input) as input_file:
    with open(args.codes) as codes_file:
      with open(args.output, 'wb') as output_file:
        sentences = []      
        for line in input_file:
          line = line.strip("\n")
          json_doc = json.loads(line)
          sentence = json_doc["codes"].split(" ")
          sentence = [str(x) for x in sentence]
          sentences.append(sentence)
        print len(sentences)
        model = gensim.models.Word2Vec(sentences, min_count=0, size=int(args.dim), workers=4)
      
        for code in codes_file:
          code = code.strip('\n')
          embedding = model[code]
          embedding = [str(x) for x in embedding]
          output_file.write(code + ":" + ",".join(embedding)+"\n")



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--input', help='path to input file to generate indexable documents from',required=True)
  parser.add_argument('--output', help='path to the output file', required=True)
  parser.add_argument('--codes', help='codes file',required=True)
  parser.add_argument('--dim', help='the dimensionality', required=True)
  args = parser.parse_args()
  main(args)