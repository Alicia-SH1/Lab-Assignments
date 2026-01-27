from Crypto.Util import number

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

message = "Hello this is the message"
print(message)

encrypted_int = encrypt(message, e, n)
print(encrypted_int)
decrypted_message = decrypt(encrypted_int, d, n)

assert decrypted_message == message
print(decrypted_message)







