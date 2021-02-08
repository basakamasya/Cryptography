# -*- coding: utf-8 -*-
"""hw2_q4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15FSrHOjSzKVeTIRDqyEjkYaxptEEQMZ2
"""

#Question 4

#taken from lfsr helper code
import copy 
import random

def LFSR(C, S):
    L = len(S)
    fb = 0
    out = S[L-1]
    for i in range(0,L):
        fb = fb^(S[i]&C[i+1])
    for i in range(L-1,0,-1):
        S[i] = S[i-1]

    S[0] = fb
    return out

def FindPeriod(s):
    n = len(s)
    for T in range(1,n+1):
        chck = 0
        for i in range(0,n-T-1):
            if (s[i] != s[i+T]):
                chck += 1
                break
        if chck == 0:
            break
    if T > n/2:
        return n
    else:
        return T        

def PolPrune(P):
    n = len(P)
    i = n-1
    while (P[i] == 0):
        del P[i]
        i = i-1
    return i

def PolDeg(P):
    n = len(P)
    i = n-1
    while (P[i] == 0):
        i = i-1
    return i

# P gets Q
def PolCopy(Q, P):
    degP = len(P)
    degQ = len(Q)
    if degP >= degQ:
        for i in range(0,degQ):
            Q[i] = P[i]
        for i in range(degQ, degP):
            Q.append(P[i])
    else: # degP < deqQ
        for i in range(0,degP):
            Q[i] = P[i]
        for i in range(degP, degQ):
            Q[i] = 0
        PolPrune(Q)           

def BM(s):
    n = len(s)

    C = []
    B = []
    T = []
    L = 0
    m = -1
    i = 0
    C.append(1)
    B.append(1)

    while(i<n):
        delta = 0
        clen = len(C)
        for j in range(0, clen):
            delta ^= (C[j]*s[i-j])
        if delta == 1:
            dif = i-m
            PolCopy(T, C)
            nlen = len(B)+dif
            if(clen >= nlen):
                for j in range(dif,nlen):
                    C[j] = C[j] ^ B[j-dif]
            else: # increase the degree of C
                for j in range(clen, nlen):
                    C.append(0)
                for j in range(dif, nlen):
                    C[j] = C[j] ^ B[j-dif]
            PolPrune(C)
            if L <= i/2:
                L = i+1-L
                m = i
                PolCopy(B, T)  
        i = i+1    
    return L, C

length = 256 #to be able to compute the period the length should be at least as twice as large as max period

L = 7
P1 = [0]*(L+1) #connection polynomials are given
P2 = [0]*(L+1)
S1 = [0]*L
P1[0] = P1[2] = P1[3] = P1[7] = 1 #1+x^2+x^3+x^7
P2[0] = P2[1] = P2[7] = 1 #1+x+x^7

max_period = 2**L - 1
print("Maximum period is:", max_period)

for i in range(0,L): # for a random initial state
    S1[i] = random.randint(0, 1)
print ("Initial state: ", S1) 

keystream1 = [0]*length
for x in range(0,length):
     keystream1[x] = LFSR(P1, S1)

keystream2 = [0]*length
for y in range(0,length):
     keystream2[y] = LFSR(P2, S1)

print("First period of P1 is: ", FindPeriod(keystream1))
#print("Linear complexity and connection polynomial", BM(keystream1))
print("First period of P2 is: ", FindPeriod(keystream2))
#print("Linear complexity and connection polynomial", BM(keystream2))
print("P1 does not generate maximum period sequences, P2 generates maximum period sequences.")