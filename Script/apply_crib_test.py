# apply_crib_test.py
cts = [bytes.fromhex(l.strip()) for l in open("mtp.txt")]
crib = b"UNLP{"
pos = 0

# construir key parcial a partir del crib usando ciphertext 0 como referencia
key = bytearray(max(len(c) for c in cts))
for i, ch in enumerate(crib):
    key[pos+i] = cts[0][pos+i] ^ ch

# aplicar key parcial y mostrar resultados
for idx,c in enumerate(cts):
    pt = bytearray()
    for j in range(len(c)):
        if key[j] != 0:
            pt.append(c[j] ^ key[j])
        else:
            pt.append(ord('?'))
    print(f"[{idx}] {pt.decode('ascii','replace')}")
