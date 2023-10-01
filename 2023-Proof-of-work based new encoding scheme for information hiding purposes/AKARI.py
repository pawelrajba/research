import numpy as np
import random
import math
import time
from scipy import stats

def randBytes(chars = [i for i in range(256)], N=8):
    return bytes([random.choice(chars) for _ in range(N)])

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

filename='akari\\nonces.txt'
f = open(filename, "r")
nonces_str = f.read()
f.close()
t = nonces_str.split()
noncesbytes = [int(t[x]) for x in range(400)]
nonces = list()
for i in range(25):
    nonces.append( noncesbytes[i*16:(i+1)*16])
    
all_content = list()
all_S = list()
all_rnd = list()
all_statistic = list()
all_pvalue = list()

rng = np.random.default_rng()

n = 25
for k in range(1,n+1):
    filenumber=k
    filename='akari\\akari.'+padzerosleft(str(filenumber),3)
    f = open(filename, "r")
    akari = f.read()
    f.close()
    t = akari.split()
    vs = bytes([int(t[x],16) for x in range(2000)])

    filename='messages\ch1.'+padzerosleft(str(filenumber),3)
    f = open(filename, "r")
    message = f.read()
    f.close()
    messagebytes = bytes(message.encode('utf-8'))

    for i in range(1,1000):
        S = nonces[k-1][0:12]
        for i in range(125):
            x1 = vs[i*16:i*16+8];
            x2 = messagebytes[i*8:(i+1)*8]
            x3 = [x1[j] ^ x2[j] for j in range(8)]
            S = S + x3

    sample1 = np.asarray(stats.uniform.rvs(0, 256, 1012, random_state=rng ), dtype = 'int').tolist()
    sample2 = list(bytes(S))
    res = stats.ks_2samp(sample1, sample2)

    all_statistic.append(res.statistic)
    all_pvalue.append(res.pvalue)

    rnd = randBytes(N=1012)

    all_content.append(entropy_new(message))
    all_S.append(entropy_new(str(bytes(S))))
    all_rnd.append(entropy_new(str(rnd)))

print(np.mean(all_statistic), np.std(all_statistic))
print(np.mean(all_pvalue), np.std(all_pvalue))
print()
print(np.mean(all_content), np.std(all_content))
print(np.mean(all_S), np.std(all_S))
print(np.mean(all_rnd), np.std(all_rnd))
print(entropy_ideal(1012))    