#Basak Amasya
#Sena Yapsu

#!pip install ecpy

#!pip install pycryptodome

import math
import timeit
import random
import sympy
import warnings
from random import randint, seed
import sys
from ecpy.curves import Curve,Point
from Crypto.Hash import SHA3_256
import requests
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import random
import re
import json
API_URL = 'http://cryptlygos.pythonanywhere.com'

stuID = 12345

curve = Curve.get_curve('secp256k1')
P = curve.generator
n = curve.order

def KeyGen():
  s = random.randint(1,n-1)
  Q = s*P
  return s, Q

def SignGen(m,sA):
  k = random.randint(1,n-1)
  R = k*P
  r = R.x % n 
  hash = str.encode(str(m)) + r.to_bytes((r.bit_length()+7)//8, byteorder='big')
  h = SHA3_256.new(hash)
  h = (int.from_bytes(h.digest(), byteorder='big')) % n
  s = (sA*h + k) % n
  return h, s

def SignVer(m,s,h,Qa):
  V = s * P - h * Qa
  v = V.x % n
  hash = str.encode(str(m)) + v.to_bytes((v.bit_length()+7)//8, byteorder='big')
  h_ = SHA3_256.new(hash)
  h_ = (int.from_bytes(h_.digest(), byteorder='big')) % n
  if h_ == h:
    return True
  else:
    return False


#HERE CREATE A LONG TERM KEY
#sL, lkey = KeyGen()
sL = 63801239034806087212362893222539508958299091046300031574693893463603277165026 #long term keys
lkey = Point(0x43ad23dc5ea14f130384d6dfa8d594dedb652c1163bba0af89a17bcebc69344 , 0x8aaa302a86c605e920bb616b21a2d6a3e2f863dacfa63d404bd2aa948b0556a2,curve)
h, s = SignGen(stuID,sL) #signing the stuID
print("h is:", h)
print("s is:", s)

#server's long term key
QSer_long = Point(0xc1bc6c9063b6985fe4b93be9b8f9d9149c353ae83c34a434ac91c85f61ddd1e9 , 0x931bd623cf52ee6009ed3f50f6b4f92c564431306d284be7e97af8e443e69a8c, curve)

# HERE GENERATE A EPHEMERAL KEY 
sA, ekey = KeyGen()
print("sA is:", sA)
print("ekey is:", ekey.x, ekey.y)
stuID = 12345

try:
  #REGISTRATION
  #mes = {'ID':stuID, 'h': h, 's': s, 'LKEY.X': lkey.x, 'LKEY.Y': lkey.y} #commented out because registration is already done
  #response = requests.put('{}/{}'.format(API_URL, "RegStep1"), json = mes)		
  #if((response.ok) == False): raise Exception(response.json())
  #print(response.json())

  #print("Enter verification code which is sent to you: ")	
  #code = int(input())


  #mes = {'ID':stuID, 'CODE': code}
  #response = requests.put('{}/{}'.format(API_URL, "RegStep3"), json = mes)
  #if((response.ok) == False): raise Exception(response.json())
  #print(response.json())



  #STS PROTOCOL

  mes = {'ID': stuID, 'EKEY.X': ekey.x, 'EKEY.Y': ekey.y}
  response = requests.put('{}/{}'.format(API_URL, "STSStep1&2"), json = mes)
  if((response.ok) == False): raise Exception(responce.json())
  res=response.json()

	#calculate T,K,U
  skey = Point(res['SKEY.X'],res['SKEY.Y'],curve)
  T = sA * skey #computing T
  print("T is:", T.x, T.y)
  U = str(T.x) + str(T.y) + "BeYourselfNoMatterWhatTheySay" #concatenating T.x, T.y and the string
  print("U is:", U)
  K = SHA3_256.new(str.encode(U)) #getting the hash
  k = K.digest()

  #Sign Message
  W1 = str(ekey.x) + str(ekey.y) + str(skey.x) + str(skey.y)
  print("W1 is:", W1)
  siga_h, siga_s = SignGen(W1,sL)
  print("h and s for W1 is:", siga_h, siga_s)

  # Encyption
  ptext = str.encode("s" + str(siga_s) + "h" + str(siga_h))
  print("ptext is:", ptext)
  cipher = AES.new(k, AES.MODE_CTR) #using k as key of the AES
  Y1 = cipher.encrypt(ptext)
  ctext = cipher.nonce + Y1
  ctext = int.from_bytes(ctext, byteorder='big')
  print("ctext is:",ctext)

  ###Send encrypted-signed keys and retrive server's signed keys
  mes = {'ID': stuID, 'FINAL MESSAGE': ctext}
  response = requests.put('{}/{}'.format(API_URL, "STSStep4&5"), json = mes)
  if((response.ok) == False): raise Exception(response.json()) 
  ctext= response.json() 

  #Decrypt
  print("Server response:", ctext)
  ctext = ctext.to_bytes((ctext.bit_length()+7)//8, byteorder='big')
  cipher = AES.new(k, AES.MODE_CTR, nonce=ctext[0:8])
  dtext = cipher.decrypt(ctext[8:])

  #verify
  dtext = dtext.decode('UTF-8')
  sigb_s = int(dtext[1:dtext.find('h')]) #finding s and h for W2 from decoded response
  sigb_h = int(dtext[dtext.find('h')+1:])
  W2 = str(skey.x) + str(skey.y) + str(ekey.x) + str(ekey.y) #constructing W2

  if SignVer(W2,sigb_s,sigb_h,QSer_long):
    print("Verified!")
  else:  #if not verified display error message and raise an exception
    print("Verification error in step 5!")
    raise Exception
   
  #get a message from server for 
  mes = {'ID': stuID}
  response = requests.get('{}/{}'.format(API_URL, "STSStep6"), json=mes)
  ctext= response.json()         
  #Decrypt

  ctext = ctext.to_bytes((ctext.bit_length()+7)//8, byteorder='big')
  cipher = AES.new(k, AES.MODE_CTR, nonce=ctext[0:8])
  dtext = cipher.decrypt(ctext[8:])
  MESSAGE = dtext.decode()
  print("Server response:", MESSAGE)
  dtext = dtext.decode()
  MESSAGE = dtext[:dtext.find('.')+1] #assuming meaningful message will always end with .
  RAND = dtext[dtext.find('.')+1:] #separating RAND and MESSAGE from .
  print("RAND is:", RAND)
  print("MESSAGE is:", MESSAGE)

  #Add 1 to random to create the new message and encrypt it
  RAND = int(RAND)+1 #adding 1 to RAND and computing the new plaintext
  ptext = str.encode(str(MESSAGE)+ " " +str(RAND))
  print("ptext is:", ptext)
  cipher = AES.new(k, AES.MODE_CTR)
  W4 = cipher.encrypt(ptext) #encrypting and adding the nonce
  W4 = cipher.nonce + W4
  ct = int.from_bytes(W4, byteorder='big')
  print("ct is:", ct)

  #send the message and get response of the server
  mes = {'ID': stuID, 'ctext': ct}
  response = requests.put('{}/{}'.format(API_URL, "STSStep7&8"), json = mes)
  ctext= response.json()  

  print("Server response:", ctext)
  ctext = ctext.to_bytes((ctext.bit_length()+7)//8, byteorder='big') #decrypting and decoding to see the final response of the server
  cipher = AES.new(k, AES.MODE_CTR, nonce=ctext[0:8])
  dtext = cipher.decrypt(ctext[8:])
  print("Decrypted text: ", dtext.decode())

except Exception as e:
 print(e)