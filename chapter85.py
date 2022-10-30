fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "mbox-short.txt"
fh = open(fname)
mail = []
for line in fh:
    if line.startswith("From ") #and len(line.split()) > 2:
        lns = line.split()
        mail.append(lns[1])
for line in mail:
    print(mail)
           
print("There were", len(mail), "lines in the file with From as the first word")
data=[]
for each in fh:
    # To check whether the line have more than two elements space seperated
    if each.startswith("From") and len(each.split())>2:
        temp=each.split()
        data.append(temp[1])
for each in data:
    print(each)
print("There were", len(data), "lines in the file with From as the first word")