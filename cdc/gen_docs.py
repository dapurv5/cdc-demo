#!/usr/bin/env/python
#
# author: apurvverma@gatech.edu

import argparse
import csv
import sys
import json
import numpy as np


def main(args):
  with open(args.input) as input_file:
    reader = csv.DictReader(input_file);
    #list of all documents from patient id -> document for that patient,
    #each document is a list of diagnostic codes
    docs = {}
    
    for row in reader:
      pid = row["DESYNPUF_ID"]
      bag_of_words = []
      if pid in docs:
        bag_of_words = docs[pid]
      
      for field_name in reader.fieldnames:
        if "DGNS_CD" in field_name and len(row[field_name]) > 0:
          bag_of_words.append(row[field_name])
      docs[pid] = bag_of_words
      wordvector = np.random.random(size=int(args.dim))

  with open(args.output, 'wb') as output_file:
    for pid, bag_of_words in docs.iteritems():
      json_doc = {'pid': pid, 'code': " ".join(bag_of_words), "wordvector": list(wordvector)}
      output_file.write(json.dumps(json_doc)+"\n")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--input',help='path to input file to generate indexable documents from',required=True)
  parser.add_argument('--output', help='path to the output file which will contain the json documents', required=True)
  parser.add_argument('--dim', help='the dimensionality of the word vector representation used for the patient', required=True)
  args = parser.parse_args()
  main(args)