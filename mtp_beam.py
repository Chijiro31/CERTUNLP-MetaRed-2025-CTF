#!/usr/bin/env python3
# mtp_beam.py
import string, heapq
from itertools import product

cts = [bytes.fromhex(l.strip()) for l in open("mtp.txt")]
max_len = max(len(c) for c in cts)
printable = set(bytes(string.printable, 'ascii'))

def score_chars(bs):
    # puntuación simple: imprimibles + letras frecuentes
    s = 0
    for b in bs:
        if b in printable: s+=1
        # puntuación adicional por letras y espacio
        if 65 <= b <= 90 or 97 <= b <= 122: s+=0.5
        if b == 32: s+=1.5
    return s

beam_width = 200  # ajustar si quieres más/menos
key_bytes = [None]*max_len
# beam: cada elemento (neg_score, key_prefix_bytes)
beam = [(0, bytearray())]

for pos in range(max_len):
    cand_heap = []
    for neg_s, prefix in beam:
        # probar todos los bytes posibles para la clave en esta posición
        for k in range(256):
            # formar pts en esta posición
            pts = []
            for c in cts:
                if pos < len(c):
                    pts.append(c[pos] ^ k)
            s = score_chars(pts)
            new_prefix = bytearray(prefix)
            new_prefix.append(k)
            # almacenar con score negativo para heapq (max heap)
            heapq.heappush(cand_heap, (-( -neg_s + s ), new_prefix))
    # quedarse con beam_width mejores
    beam = heapq.nsmallest(beam_width, cand_heap)
    print(f"pos {pos} beam best score {-beam[0][0]}")
# al final, mostrar mejor clave
best_key = beam[0][1]
print("Mejor key (hex):", best_key.hex())
print("Mejor key (ascii, parcial):", best_key.decode('ascii','replace'))
# descifrar
for i,c in enumerate(cts):
    pt = bytes([ c[j] ^ best_key[j] for j in range(len(c)) ])
    print(f"[{i}] {pt.decode('ascii','replace')}")
