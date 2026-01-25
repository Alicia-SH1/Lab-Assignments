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

def encrypt(plaintext, e, n):
    m = int(plaintext.encode('ascii').hex(),16)
    return pow(m,e,n)
def decrypt(cipher_int, d, n):
    m = pow(cipher_int, d, n)
    return bytes.fromhex(hex(m)[2:]).decode('ASCII')

keys = generate_keys(128)
n = keys[0]
e = keys[1]
d = keys[2]

# This doesn't really get used
c = encrypt("THIS IS BOB'S SECRET KEY", e, n)

c_prime = n
iv = b"1234567890123456"

alice_calculated_s = pow(c_prime, d, n)
mallory_s = 0

alice_key = hashlib.sha256(str(alice_calculated_s).encode()).hexdigest()
mallory_key = hashlib.sha256(str(mallory_s).encode()).hexdigest()

alice_key = str(alice_key)[:16].encode()
mallory_key = str(mallory_key)[:16].encode()

cipher = AES.new(alice_key, AES.MODE_CBC,iv=iv)
mallory_decrypt_cipher = AES.new(mallory_key, AES.MODE_CBC, iv=iv)

message = "Hello Bob"
message = pad(str.encode(message),16)

alice_encrypted_message = cipher.encrypt(message)

mallory_decrypted_message = unpad(mallory_decrypt_cipher.decrypt(alice_encrypted_message), 16)

print(mallory_decrypted_message)












