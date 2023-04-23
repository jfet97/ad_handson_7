# paths utils

class Dataset():
  def __init__(self, path, sizes):
    self.path = path
    self.sizes = sizes

class HandsonDatasets:
  SMALL = Dataset("mini.csv", [5000, 40, 5000, 144])
  MEDIUM = Dataset("sample.csv", [12000, 400, 30000, 144])
  HUGE = Dataset("output.csv", [250000, 400, 700000, 144])


  
# For question number 1 I've taken size from the table on the slides
# For question 2 I made lot of attemtps to find a right size,
# I don't know how to estimate it
