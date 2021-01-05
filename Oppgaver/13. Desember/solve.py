ct = open("melding.txt","r").read()
lines = ct.split("\n")
ct = ct.replace("\n","")

chars = "0123456789ABCDEF"
freq = {i:ct.count(i) for i in chars}

for i in lines:
    print("".join("*" if freq[j] < 100 else " " for j in i))
