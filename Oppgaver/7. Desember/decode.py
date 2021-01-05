
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
