import math
from datetime import date

# definerer en klasse Date for å holde kontroll på datoen
class Date:
    def __init__(self,d,m,y):
        self.d = d
        self.m = m
        self.y = y
        pass
    def dateAdd(self,v,a):
        if v=="d":
            self.d+= a
        elif v=="m":
            self.m+=a
        elif v=="y":
            self.y+=a
    def __repr__(self):
        return str(self.d)+"/"+str(self.m)+"/"+str(self.y)
    def toInt(self):
    	# brukte datetime til å kalkulere antall dager
        s = date(1899,1,1)
        d = date(self.y,self.m,self.d)
        
        return (d-s).days

# dbo.FunctionPaaskeAften.sql konvertert til python
def FunctionPaaskeAften(aar):
    a = aar%19
    b = math.floor(aar/100)
    c = aar%100
    d = math.floor(b/4)
    e = b%4
    f = math.floor((8+b)/25)
    g = math.floor((1+b-f)/3)
    h = (19*a+b-d-g+15)%30
    i = math.floor(c/4)
    k = aar%4
    l = (32+2*e+2*i-h-k)%7
    m = math.floor((a+11*h+22*l)/451)
    easterday = Date(1,1,2000)
    easterday.dateAdd("y",aar-2000)
    easterday.dateAdd("m",math.floor((h+l-7*m+114)/31)-1)
    easterday.dateAdd("d",(h+l-7*m+114)%31)

    return easterday

# printer summen av Maaltallene fra påskeaften 2020 til og med påskeaften 2040, omringet av PST{.*}
print("PST{",sum([FunctionPaaskeAften(i).toInt()-366 for i in range(2020,2041)]),"}",sep="")
