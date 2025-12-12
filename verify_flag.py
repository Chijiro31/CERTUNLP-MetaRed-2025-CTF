cts = [bytes.fromhex(l.strip()) for l in open("mtp.txt")]
key = b"UNLP{we_4llLiv3inTheS4m3CountryCall3dCapitalism}"
for i,c in enumerate(cts):
    pt = bytes([ c[j] ^ key[j] for j in range(len(c)) ])
    print(f"[{i}] {pt.decode('ascii','replace')}")
