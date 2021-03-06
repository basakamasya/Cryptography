# -*- coding: utf-8 -*-
"""hw3_q2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YEBPh06peCa5Ju4RXfyyKAcy8WbHB9wH
"""

#Question 2
import itertools
import copy 

#taken from helper code
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

z = [0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1]
#z = [0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
C1 = [0] * 15
C2 = [0] * 18
C3 = [0] * 12
C1[0] = C1[5] = C1[14] = 1 #connection polynomials
C2[0] = C2[3] = C2[17] = 1
C3[0] = C3[2] = C3[11] = 1
length = len(z)

states1 = list(itertools.product([0, 1], repeat=14)) #all possible initial states for the LFSRs
states2 = list(itertools.product([0, 1], repeat=17))
states3 = list(itertools.product([0, 1], repeat=11))

def checkcorrelation(C,states): #correlation attack
  possiblestates = []
  possiblekeys = []
  for S in states:
    keystream = [0]*length
    initialstate = list(S)
    for i in range(0,length): #constructing the keystream
      keystream[i] = LFSR(C, initialstate)
    count = 0
    for j in range(0,length):
      if z[j] == keystream[j]:
        count += 1 #count number of coincidences
    if count > 75 or C == C2: #if above the threshold for LFSR1 and LFSR3, take all for LFSR2
      possiblestates.append(list(S))
      possiblekeys.append(keystream)
      #print("When initial state is", list(S), "correlation is", count, "/", length)
  return possiblestates, possiblekeys

possiblestates1, possiblekeys1 = checkcorrelation(C1,states1) 
possiblestates2, possiblekeys2 = checkcorrelation(C2,states2)
possiblestates3, possiblekeys3 = checkcorrelation(C3,states3)
#print(len(possiblestates1))
#print(len(possiblestates2))
#print(len(possiblestates3))

for l in range(len(possiblekeys1)):
  for j in range(len(possiblekeys2)):
    for k in range(len(possiblekeys3)):
      F = [0] * length
      x1 = possiblekeys1[l]
      x2 = possiblekeys2[j]
      x3 = possiblekeys3[k]
      for i in range(length):
        F[i] = x1[i]&x2[i] ^ x2[i]&x3[i] ^ x3[i]
        if F[i] != z[i]: #not necessary to go on if the corresponding bits are not same
          break
      if F == z: #generated the output
        #print(F)
        print("Key stream of LFSR1 is:", x1)
        print("Key stream of LFSR2 is:", x2)
        print("Key stream of LFSR1 is:", x3)
        print("Initial state of LFSR1 is", possiblestates1[l]) #corresponding index is the state
        print("Initial state of LFSR2 is", possiblestates2[j])
        print("Initial state of LFSR3 is", possiblestates3[k])


#Checking if key streams really construct F
#F2 = [0] * length
#x1 = [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1]
#x2 = [0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1]
#x3 = [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0]
#for i in range(length):
#        F2[i] = x1[i]&x2[i] ^ x2[i]&x3[i] ^ x3[i]
#print(F2 == z)

#S1 = [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1]
#S2 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]
#S3 = [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0]
#key1 = [0] * length
#key2 = [0] * length
#key3 = [0] * length

#Checking if these initial states really construct those keys
#for a in range(0,length):
#      key1[a] = LFSR(C1, S1)
#for b in range(0,length):
#      key2[b] = LFSR(C2, S2)
#for c in range(0,length):
#      key3[c] = LFSR(C3, S3)
#print(key1 == x1)
#print(key2 == x2)
#print(key3 == x3)