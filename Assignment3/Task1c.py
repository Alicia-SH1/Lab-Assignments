import hashlib
import time
from bitstring import Bits

def mod_sha256(s,bits):
    bit_hash = Bits(bytes=hashlib.sha256(s.encode()).hexdigest().encode())
    return bit_hash[:bits]

def hash_brute_force(s):
    for num_bits in range(46,52,2):
        i = 0
        target_hash = mod_sha256(s,num_bits)
        start = time.time()
        while True:
            if mod_sha256(str(i),num_bits) == target_hash:
                print("bit {} found at i: {}".format(num_bits,i))
                end = time.time()
                print("Time taken: {}".format(end-start))
                break
            i += 1

def hash_brute_force2(s):
    i = 0
    target_hash = mod_sha256(s,50)
    start = time.time()
    while True:
        if mod_sha256(str(i), 50) == target_hash:
            print("bit {} found at i: {}".format(50, i))
            end = time.time()
            print("Time taken: {}".format(end - start))
            break


print(hash_brute_force('hello'))
