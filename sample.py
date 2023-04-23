import random
import csv
import codecs

def quote(col):
    if col is None:
        return '\"\"'
    # uses double-quoting style to escape existing quotes
    return '\"' + col + '\"'

if __name__ == "__main__":
  o = open ("output.csv", "w")
  with codecs.open("training.1600000.processed.noemoticon.csv", 'r', encoding='ascii',
                   errors='ignore') as f:
      reader = csv.reader (f) 
      for line in reader:
        if line[0] == "0":
            line[0] = "-"
        else:
            line[0] = "+"
        del line[3]
        del line[1]
        o.write (", ".join (map(quote, line)) + "\n")

o.close ()
