import json
import hashlib
  

# les filen (utf-8 enkoding tillater bruk av æøå)
f = open('snille.json',encoding="utf-8",)

# leser data som json
data = json.load(f) 

# itererer igjennom radene
for i in data:
    m = hashlib.md5()
    # henter fornavn
    fornavn = i["fornavn"]
    # henter etternavn
    etternavn = i["etternavn"]
    # tar md5-sum av fornavn og etternavn
    m.update(fornavn.encode()+etternavn.encode())
    # få ut som hex
    h = m.hexdigest()
    # sjekk om md5 matcher den i fila
    if h!=i["md5"]:
        # hvis ikke, print ut
        print(fornavn,etternavn,h,i["md5"])

f.close() 
