# funksjon som skifter alle bokstaver i input med 1 (A -> B, B -> C, osv.)
def rot1(n):
    # variabel for sluttresultat
    res = ""
    # løkker over alle bokstaver i chiffertekst
    for i in n:
        c = ord(i)
        # I ASCII-enkoding, så er kodene 65-90 og 96-122 bokstaver (store og små respektivt)
        if (c>64 and c<90) or (c>96 and c<122):
            res += chr(c+1)
        # for bokstaven Z vil vi gå tilbake til A, så vi trekker fra 25 istedet for å legge til 1
        elif c==90 or c==122:
            res += chr(c-25)
        # hvis tegnet ikke er en bostav-legger vi det bare till sluttresultatet uten å endre noe
        else:
            res+=i
    return res
# funksjon for å dekryptere, "n" er teksten vi vil dekryptere,
# "crib" er deler av teksten vi allerede vet
def rot(n, crib):
    # denne while-løkken sjekker om n inneholder crib, hvis ikke skiftes alle bokstavene med 1
    # på denne måten kan vi raskt dekryptere teksten uten å måtte gjette oss fram
    while not crib in n:
        n = rot1(n)
    return n
        
# vi vet at flagget starter med "PST", så nå trenger vi bare å bruke funksjonen til å finne hvor mange
# bokstaver i alfabetet vi må skifte chifferteksten med
print(rot("RUV{JgkJqPåGtFgvLwnKilgp}","PST"))
