from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib

q_literal = "B10B8F96 A080E01D DE92DE5E AE5D54EC 52C99FBC FB06A3C6 9A6A9DCA 52D23B61 6073E286 75A23D18 9838EF1E 2EE652C0 13ECB4AE A9061123 24975C3C D49B83BF ACCBDD7D 90C4BD70 98488E9C 219A7372 4EFFD6FA E5644738 FAA31A4F F55BCCC0 A151AF5F 0DC8B4BD 45BF37DF 365C1A65 E68CFDA7 6D4DA708 DF1FB2BC 2E4A4371"
g_literal = "A4D1CBD5 C3FD3412 6765A442 EFB99905 F8104DD2 58AC507F D6406CFF 14266D31 266FEA1E 5C41564B 777E690F 5504F213 160217B4 B01B886A 5E91547F 9E2749F4 D7FBD7D3 B9A92EE1 909D0D22 63F80A76 A6A24C08 7A091F53 1DBF0A01 69B6A28A D662A4D1 8E73AFA3 2D779D59 18D08BC8 858F4DCE F97C2A24 855E6EEB 22B3B2E5"

q_literal = q_literal.replace(" ", "")
g_literal = g_literal.replace(" ", "")

q = int(q_literal, 16)
g = int(g_literal, 16)

def get_public_key(secret):
    return pow(g, secret, q)

def get_shared_key(secret, other_public):
    return pow(other_public,secret, q)

x_a = 5
x_b = 10

public_key_a = get_public_key(x_a)
public_key_b = get_public_key(x_b)

shared_key_a = get_shared_key(x_a, public_key_b)
shared_key_b = get_shared_key(x_b, public_key_a)

print(shared_key_a)
print(shared_key_b)
assert shared_key_a == shared_key_b

message = pad(str.encode("encrypt this message"),16)

sha_shared_key = hashlib.sha256(str(shared_key_a).encode()).hexdigest()

truncated_key = str(sha_shared_key)[:16].encode()

iv = get_random_bytes(16)

cipher_a = AES.new(truncated_key, AES.MODE_CBC,iv=iv)
cipher_b = AES.new(truncated_key, AES.MODE_CBC,iv=iv)

encrypted_message_a = cipher_a.encrypt(message)
encrypted_message_b = cipher_b.encrypt(message)

decipher_a = AES.new(truncated_key, AES.MODE_CBC,iv=iv)
decipher_b = AES.new(truncated_key, AES.MODE_CBC,iv=iv)

decrypted_message_a = unpad(decipher_a.decrypt(encrypted_message_a),16)
decrypted_message_b = unpad(decipher_b.decrypt(encrypted_message_b),16)

assert decrypted_message_a == decrypted_message_b

print(decrypted_message_a)



