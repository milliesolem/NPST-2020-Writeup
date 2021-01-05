code = """ [0] (1 elem)
 INTEGER 3
 [1] (1 elem)
 INTEGER 12
 [2] (1 elem)
 INTEGER 0
 [1] (1 elem)
 INTEGER 19
 [0] (1 elem)
 INTEGER 1
 [1] (1 elem)
 INTEGER 18
 [4] (1 elem)
 NULL
 [1] (1 elem)
 INTEGER 20
 [1] (1 elem)
 INTEGER 14
 [2] (1 elem)
 INTEGER 24
 [1] (1 elem)
 INTEGER 4
 [1] (1 elem)
 INTEGER 18
 [1] (1 elem)
 INTEGER 14
 [1] (1 elem)
 INTEGER 14
 [1] (1 elem)
 INTEGER 7
 [2] (1 elem)
 INTEGER 2
 [2] (1 elem)
 INTEGER 8
 [0] (1 elem)
 INTEGER 1
 [2] (1 elem)
 INTEGER 13
 [2] (1 elem)
 INTEGER 18
 [2] (1 elem)
 INTEGER 0
 [3] (1 elem)
 NULL
 [2] (1 elem)
 INTEGER 19
 [2] (1 elem)
 INTEGER 18
 [2] (1 elem)
 INTEGER 15
 [1] (1 elem)
 INTEGER 17
 [1] (1 elem)
 INTEGER 14
 [1] (1 elem)
 INTEGER 11
 [0] (1 elem)
 INTEGER 0
 [2] (1 elem)
 INTEGER 3
 [1] (1 elem)
 INTEGER 12
 [1] (1 elem)
 INTEGER 20
 [1] (1 elem)
 INTEGER 18
 [1] (1 elem)
 INTEGER 15
 [0] (1 elem)
 INTEGER 1
 [1] (1 elem)
 INTEGER 12
 [0] (1 elem)
 INTEGER 3
 [1] (1 elem)
 INTEGER 17
 [1] (1 elem)
 INTEGER 14
 [2] (1 elem)
 INTEGER 11
 """.split("\n")

res = ""
alphabet="abcdefghijklmnopqrstuvwxyz"
digit = "0123456789"
for i in range(0,len(code),2):
    if "[0]" in code[i]:
        res+=digit[int(code[i+1].split(" ")[2])]
    if "[1]" in code[i]:
        res+=alphabet[int(code[i+1].split(" ")[2])]
    if "[2]" in code[i]:
        res+=alphabet[int(code[i+1].split(" ")[2])].upper()
    if "[3]" in code[i]:
        res+="{"
    if "[4]" in code[i]:
        res+="}"
print(res[::-1])


