#!/usr/bin/env/python
#
# author: apurvverma@gatech.edu

class Visit(object):
  def __init__(self):
    self.admission_date = None
    self.discharge_date = None
    self.codes = "" #all codes for the patient in this visit
    
  def add_code(self, code):
    self.codes = self.codes + " " + code
    self.codes = self.codes.strip()


class Patient(object):
  def __init__(self):
    self.pid = -1
    self.codes = "" #all codes of this patient
    self.visits = [] #list of visits by a patient
  
  def add_visit(self, visit):
    self.visits.append(visit)
    self.codes = self.codes + " " + visit.codes
    self.codes = self.codes.strip()
    