import hashlib


def get_hamming_distance_one(message):
    bit_message = bytearray(message.encode())
    bit_index = 0

    bit_message[0] ^= 1 << bit_index

    result = bytes(bit_message)
    return result



arbitrary_string = "hello world"

hash_hex = hashlib.sha256(arbitrary_string.encode()).hexdigest()

ham_distance_one = get_hamming_distance_one(arbitrary_string)

hash_hex_2 = hashlib.sha256(ham_distance_one).hexdigest()

print(hash_hex_2)
print(hash_hex)

