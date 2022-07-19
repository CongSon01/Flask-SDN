if (1 < 4 < 3):
    print("ok")



sent = 1000556 - 1000000
byteReceived = 37055712 - 1000000
print(sent, byteReceived)
print(sent+byteReceived)
sum  = sent+byteReceived
print(sum*8)
overhead = ( (sent + byteReceived * 8)) / 1000000  # convert byte/s => Mb/s
print(overhead)
a = 20 * 10**6 / 8
print(a)

print(10**-6)