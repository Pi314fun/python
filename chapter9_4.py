name = input("Enter file:")
if len(name) < 1:
    name = "mbox-short.txt"
handle = open(name)
counts = dict()

for line in handle:
    if line.startswith("From "): 
        words = line.split()
        counts[words[1]] = counts.get(words[1], 0) + 1
#print(counts)
bigcount = None
bigword = None
for key in counts:
    if bigcount is None:
        bigcount = counts[key]
        #print(bigcount)
    elif counts[key] > bigcount:   
        bigcount = counts[key]
        bigword = key
        
print(bigword, bigcount)
