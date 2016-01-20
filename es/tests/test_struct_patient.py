#!/usr/bin/env/python
#
# author: apurvverma@gatech.edu


import unittest
import json

from es.common import Patient
from es.common import Visit

class PatientTest(unittest.TestCase):

  def test_patient_to_json(self):
    p = Patient()
    p.pid = "1"
    
    v1 = Visit()
    v1.admission_date = "20150602"
    v1.discharge_date = "20150608"
    v1.add_code("123")
    
    p.add_visit(v1)
    #to convert it to a json object
    print json.dumps(p, default=lambda o: o.__dict__)
