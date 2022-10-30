import re

fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "sample.txt"
fh = open(fname)
total = list()
for line in fh:
    subtotal = re.findall('[0-9]+',line) 
    total = total + subtotal
sum = 0
for i in total:
    sum = sum + int(i)
print(sum)
    