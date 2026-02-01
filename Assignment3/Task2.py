from concurrent.futures import ThreadPoolExecutor
import bcrypt
import nltk
from nltk.corpus import words
import time

arr = words.words()

arr = [x for x in arr if 6 <= len(x) <= 10]
saltHashes = [["" for _ in range(2)] for _ in range(15)]
with open("pass") as f:
    index = 0
    for line in f:
        string = line.split('$')
        salt = string[1] + "$" +  string[2] + "$" + string[3][:22]
        hash = string[3][22:]
        saltHashes[index][0] = salt
        saltHashes[index][1] = hash
        index+=1
def worker(startIndex, endIndex, salt, hash):
    start = time.time()
    currIndex = startIndex
    while currIndex < endIndex:
        if currIndex % 1000 == 0:
            print(currIndex)
        word = arr[currIndex].encode()
        res = bcrypt.hashpw(word,salt.encode())
        res = res[29:]
        for j in range(len(hash)):
            h = hash[j][:-1]
            if h.encode() == res:
                end = time.time()
                with open("answers","a") as f:
                    f.write("word: {} , time: {}\n".format(word,end-start))
        currIndex+=1
threads = 50
part = (len(arr) // threads) + 1
saltMap = [1,3,5,8,11,14]
hashMap = [[0,1,2],[3,4],[5,6,7],[8,9,10],[11,12,13],[14]]

currIndex = 5

saltMapIndex = saltMap[currIndex]
salt = saltHashes[saltMapIndex][0]
hashes = [saltHashes[j][1] for j in hashMap[currIndex]]

start = 0
# len(arr) = 135145
with ThreadPoolExecutor(max_workers=threads) as executor:
    results = []
    for i in range(threads):
        if start + part > len(arr):
            end = len(arr)
        else:
            end = start + part
        executor.submit(worker,start,end,salt,hashes)
        start += part

