file = open("pen_gwyn_greatest_hits.mid","rb").read()
flag_start = file.index(b"P")
flag_end = file.index(b"}")
interval = 10
print(file[flag_start:flag_end+interval:interval].decode())
