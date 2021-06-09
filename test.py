import re

string = 'cs2040'
m = re.match(r"(\D{2,3}\d{2,4})", mystring)
start, stop = m.span()
if stop-start == len(mystring):
    print("The entire string matched"

