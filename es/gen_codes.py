#!/usr/bin/env/python

"""
Writes all the codes in an output file
The file produced is sorted by codes
"""
import argparse
import json

def main(args):
  uniq_codes = set()
  with open(args.input) as input_file:
    for line in input_file:
      json_doc = json.loads(line)
      codes = json_doc["codes"]
      for code in codes.split(" "):
        uniq_codes.add(code)

  uniq_codes = sorted(uniq_codes)
  with open(args.output, 'wb') as output_file:
    for code in uniq_codes:
      output_file.write(code + "\n")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--input', help='path to input file to generate indexable documents from',required=True)
  parser.add_argument('--output', help='path to the output file')
  args = parser.parse_args()
  main(args)