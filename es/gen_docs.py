#!/usr/bin/env/python
#
# author: apurvverma@gatech.edu
#
# Reads the claims file and generates json patient data from it
# 

import argparse
import csv
import json

from common import Patient
from common import Visit

def main(args):
  with open(args.input) as input_file:
    reader = csv.DictReader(input_file);
    patients = {} #map from patient_id -> Patient() object
    
    for row in reader:
      pid = row["DESYNPUF_ID"]
      if pid not in patients:
        patient = Patient()
        patient.pid = pid
        patients[pid] = patient
      patient = patients[pid]
      
      visit = Visit()
      for field_name in reader.fieldnames:
        value = row[field_name]
        if "DGNS_CD" in field_name and len(row[field_name]) > 0:
          visit.add_code(value)
        elif "CLM_FROM_DT" in field_name and  len(row[field_name]) > 0:
          visit.admission_date = value
        elif "CLM_THRU_DT" in field_name and len(row[field_name]) > 0:
          visit.discharge_date = value           
      patient.add_visit(visit)
      patients[pid] = patient

  with open(args.output, 'wb') as output_file:
    for pid, patient in patients.iteritems():
      output_file.write(json.dumps(patient, default=lambda o: o.__dict__)+"\n")

#python gen_docs.py --input /home/dapurv5/Desktop/Semesters/Semester2/GRA/Data/DE1_0_2008_to_2010_Inpatient_Claims_Sample_2.csv
#                   --output /mnt/production/cdc/gen_docs/docs.json
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Specify arguments')
  parser.add_argument('--input',help='path to input file to generate indexable documents from',required=True)
  parser.add_argument('--output', help='path to the output file which will contain the json documents', required=True)
  args = parser.parse_args()
  main(args)
