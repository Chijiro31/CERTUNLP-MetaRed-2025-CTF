1) Preparación (requisitos)

Instala Python 3 y estos paquetes (opcional, los scripts funcionan sin paquetes externos):

# opcional: crear virtualenv
python3 -m venv venv && source venv/bin/activate

# instalar (no obligatorio)
pip install numpy


Coloca tu mtp.txt en el mismo directorio donde ejecutarás los scripts.

2) Script rápido: deducción por puntuación (funciona bien como primer intento)

Guarda como mtp_solve_simple.py:
```
#!/usr/bin/env python3
# mtp_solve_simple.py
import string

# cargar
cts = [bytes.fromhex(l.strip()) for l in open("mtp.txt")]
N = len(cts)
max_len = max(len(c) for c in cts)

# printable score
printable = set(bytes(string.printable, 'ascii'))
def score(bs):
    return sum(1 for b in bs if b in printable)

# intentar cada posición: elegir byte de clave que maximice chars imprimibles
key = bytearray([0]*max_len)
for pos in range(max_len):
    best_k = 0
    best_s = -1
    for k in range(256):
        pts = []
        for c in cts:
            if pos < len(c):
                pts.append(c[pos] ^ k)
        s = score(pts)
        if s > best_s:
            best_s = s
            best_k = k
    key[pos] = best_k

print("Key (hex):", key.hex())
try:
    print("Key (ascii):", key.decode())
except:
    print("Key ascii not fully printable.")

# descifrar
for i,c in enumerate(cts):
    pt = bytes([ c[j] ^ key[j] for j in range(len(c)) ])
    print(f"[{i}] {pt.decode('ascii','replace')}")
```
