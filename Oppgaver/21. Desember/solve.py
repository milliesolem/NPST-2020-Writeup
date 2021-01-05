
rule={}

gen0 = "01010000010100110101010001111011"
gen1 = "010110001101110101010110100010010001111101011101000100110101110100011111100111011101101100110111101001100101110101000001001101011101110100100110101001101001010100100110010101101001111111000001110101101001010100010110010110001010010111010110100101100101100010100011100111011100000100000101"

# lager liste av gen1 med samme lengde som gen0
# gjør det lett å sammenligne gen0 og gen1 siden
# det siste elementet av denne listen vil høre til
# det siste elementet i gen0
subgen1 = gen1[:len(gen0)]

# genererer regel ved å sammenligne gen1 og gen0
def genrule(g0,g1):
    for i in range(len(g0)-2):
        rule[g0[i:i+3]] = g1[i+1]

# bygger gen0 ved bruk a gen1
def getflag(g0,sg1,g1):
    while len(g0) < len(g1):
        a = g0[-2:]
        if rule[a+"0"]==sg1[-1]:
            g0+="0"
        else:
            g0+="1"
        sg1 += g1[len(sg1)]
    return g0

# converterer binærtall til ascii
def bin2ASCII(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

# kjør funksjonene og print flagget
genrule(gen0,gen1)
gen0 = getflag(gen0,subgen1,gen1)
flag = bin2ASCII(gen0)

print(flag)
