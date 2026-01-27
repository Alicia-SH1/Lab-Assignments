# Write signature and verification

def sign(m,d,n):
    return pow(m,d,n)

d = 13
n = 221

m1 = sign(123123, d, n)
m2 = sign(456456, d, n)

forged_signature = (m1 * m2) % n

m3 = sign(123123 * 456456,d,n)

print(forged_signature)
print(m3)

print(forged_signature == m3)

