file = open("log_formatted.csv","rb").read().decode()

senders = {}

for i in file.split("\n")[:-1]:
    f = i.split(";")
    if f[1] in senders.keys():
        senders[f[1]] = ""
    else:
        senders[f[1]] = i
for j in senders.keys():
    if senders[j]!="":
        print(senders[j])
