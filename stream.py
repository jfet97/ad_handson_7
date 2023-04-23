import csv, re, string
from enum import Enum

class dayPart(Enum):
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    NIGHT = 4
    UNKNOWN = 5
  
class mystream:
  def __init__(self, filePath="sample.csv"):
    self.pf = open (filePath, newline='') 
    self.reader = csv.reader (self.pf) # Create csv reader for f
    self.currentline = None
    
  def nextRecord (self):
    try:
      self.currentline = next(self.reader)
      return self.currentline
    except:
      self.currentline = None
      return None

  def timeBin (self):
    m = re.search('[0-9]+:[0-9]+:[0-9]+', self.currentline[1])
    if not m:
      return dayPart.UNKNOWN
    m = re.search('[0-9]+', m.group ())
    if not m:
      return dayPart.UNKNOWN
    h = int (m.group ())
    if h >= 7 and h < 13:
      return dayPart.MORNING
    elif h >= 14 and h < 19:
      return dayPart.AFTERNOON
    elif h >= 19 and h < 23:
      return dayPart.EVENING         
    else:
      return dayPart.NIGHT
    
  def ispositive (self):
    if self.currentline[0] == "+":
      return True
    return False

  def username (self):
    return self.currentline[2]

  def isnegative (self):
    if self.currentline[0] == "-":
      return True
    return False

  def tokenizedTweet (self):
    r = "".join ([" " for i in range (len (string.punctuation))])
    out = self.currentline[3].translate(str.maketrans(string.punctuation,r))
    return out.split ()
  
  def reset(self):
    self.pf.seek(0)
    self.reader = csv.reader(self.pf)
    