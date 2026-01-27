import hashlib
from Crypto.Util import number
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


# Provided by Yocam
def mod_inverse(a, m):
    def egcd(a,b):
        if a == 0: return b, 0, 1
        else:
            g,y,x = egcd(b % a, a)
            return g, x - (b // a) * y, y
    g,x, _ = egcd(a,m)
    if g != 1: raise Exception('modular inverse does not exist')
    else: return x % m

def generate_keys(bits_prime_length):
    if bits_prime_length > 2048:
        raise TypeError("Bit length must be <= 2048")
    p = number.getPrime(bits_prime_length)
    q = number.getPrime(bits_prime_length)
    n = p * q
    phi = (p-1) * (q-1)
    e = 65537
    d = mod_inverse(e, phi)

    return n,e,d

def encrypt(m, e, n):
    return pow(m,e,n)
def decrypt(cipher_int, d, n):
    return pow(cipher_int, d, n)
def s_prime_brute_forcer(encrypted_message, init_vec):
    i = 0
    while True:
        key = hashlib.sha256(str(i).encode()).hexdigest()
        key = str(key)[:16].encode()
        cipher2 = AES.new(key, AES.MODE_CBC, iv=init_vec)
        if cipher2.decrypt(encrypted_message)[:len("Hello Bob")] == b"Hello Bob": # This line would probably check for normal texts if you don't know the message.
            return i
        i += 1

keys = generate_keys(512)
n = keys[0]
e = keys[1]
d = keys[2]

original_s = 7987
r = 2

c = encrypt(original_s, e, n)

c_prime = (c * pow(r,e)) % n

iv = b"1234567890123456"

s_prime = decrypt(c_prime, d, n)

alice_key = hashlib.sha256(str(s_prime).encode()).hexdigest()

alice_key = str(alice_key)[:16].encode()

cipher = AES.new(alice_key, AES.MODE_CBC,iv=iv)

message = "Hello Bob"
message = pad(str.encode(message),16)

alice_encrypted_message = cipher.encrypt(message)

calc_s_prime = s_prime_brute_forcer(alice_encrypted_message, init_vec=iv)
r_inverse = mod_inverse(r, n)
calculated_s = (calc_s_prime * r_inverse) % n

print(calculated_s)
print(original_s)

assert calculated_s == original_s








