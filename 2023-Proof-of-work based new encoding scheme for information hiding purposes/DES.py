from Crypto.Cipher import DES
import time
import random
import string
import hashlib
import math
import numpy as np
from scipy import stats

def entropy_new(string):
    "Calculates the Shannon entropy of a string"
    # get probability of chars in string
    prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
    # calculate the entropy
    entropy_new = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
    return entropy_new

def entropy_ideal(length):
    "Calculates the ideal Shannon entropy of a string with given length"
    prob = 1.0 / length
    return -1.0 * length * prob * math.log(prob) / math.log(2.0)

def padzerosleft(text,length):
    n = len(text)
    return ('0'*(length-n))+text    
    
def padspacesright(text):
    n = 8-len(text) % 8
    if (n==8):
        n=0
    return text + (b' ' * n)

def randStr(chars = string.ascii_uppercase + string.digits, N=8):
    return ''.join(random.choice(chars) for _ in range(N))

def encr(key, iv, text):
    des_e = DES.new(key, mode=DES.MODE_CBC, iv=iv)
    padded_text = padspacesright(text)
    return des_e.encrypt(padded_text)

def decr(key, iv, encrypted_text):
    des_d = DES.new(key, mode=DES.MODE_CBC, iv=iv) #DES.MODE_ECB)
    return des_d.decrypt(encrypted_text)

def randStr(chars = [chr(i) for i in range(256)], N=8):
    return ''.join(random.choice(chars) for _ in range(N))

def randBytes(chars = [i for i in range(256)], N=8):
    return bytes([random.choice(chars) for _ in range(N)])

def hashfun(text):
    return hashlib.sha256(text.encode('utf-8')).digest()

key = b'00000001'
iv = randBytes()

#rnd = randBytes(N=1040)

all_content = list()
all_S = list()
all_rnd = list()
all_statistic = list()
all_pvalue = list()

rng = np.random.default_rng()

n = 25
for i in range(1,n+1):
    filenumber=i
    filename='messages\ch1.'+padzerosleft(str(filenumber),3)
    f = open(filename, "r")
    content = f.read()
    f.close()

    for i in range(1,1000):
        S=iv+hashfun(str(iv+key))+encr(key, iv, bytes(content.encode('utf-8')))

    for i in range(1,1000):
        rec_iv = S[0:8]
        rec_hash = S[8:40]
        rec_encrypted = S[40:]
        rec_key = ""

        for i in range(0,99999999,1):
            rec_key = bytes(padzerosleft(str(i),8).encode('utf-8'))
            test_hash = hashfun(str(rec_iv+rec_key))
            if (test_hash==rec_hash):
                break

        rec_content = decr(rec_key,rec_iv,rec_encrypted)

    sample1 = np.asarray(stats.uniform.rvs(0, 256, 1040, random_state=rng ), dtype = 'int').tolist()
    sample2 = list(S)
    res = stats.ks_2samp(sample1, sample2)

    all_statistic.append(res.statistic)
    all_pvalue.append(res.pvalue)

    rnd = randBytes(N=1040)

    all_content.append(entropy_new(content))
    all_S.append(entropy_new(str(S)))
    all_rnd.append(entropy_new(str(rnd)))

print(np.mean(all_statistic), np.std(all_statistic))
print(np.mean(all_pvalue), np.std(all_pvalue))
print()
print(np.mean(all_content), np.std(all_content))
print(np.mean(all_S), np.std(all_S))
print(np.mean(all_rnd), np.std(all_rnd))
print(entropy_ideal(1040))
