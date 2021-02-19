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

from Crypto.Hash import HMAC, SHA256


API_URL = 'http://cryptlygos.pythonanywhere.com'

stuID =  12345  ## 24198, 19872, 23574, 25655

#Functions
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


#create a long term key
sL = 63801239034806087212362893222539508958299091046300031574693893463603277165026
QCli_long = Point(0x43ad23dc5ea14f130384d6dfa8d594dedb652c1163bba0af89a17bcebc69344 , 0x8aaa302a86c605e920bb616b21a2d6a3e2f863dacfa63d404bd2aa948b0556a2,curve)
h, s = SignGen(stuID,sL) #signing the student ID
print("h is", h)
print("s is", s)

#server's long term key
QSer_long = Point(0xc1bc6c9063b6985fe4b93be9b8f9d9149c353ae83c34a434ac91c85f61ddd1e9 , 0x931bd623cf52ee6009ed3f50f6b4f92c564431306d284be7e97af8e443e69a8c, curve)

####Register Long Term Key
#mes = {'ID':12345, 'H': h, 'S': s, 'LKEY.X': QCli_long.x, 'LKEY.Y': QCli_long.y} #commented out because already registered
#response = requests.put('{}/{}'.format(API_URL, "RegLongRqst"), json = mes)
#print(response.json())
#code = input()

#mes = {'ID':12345, 'CODE': code}
#response = requests.put('{}/{}'.format(API_URL, "RegLong"), json = mes)
#print(response.json())

###delete ephemeral keys
mes = {'ID': stuID, 'S': s, 'H': h}
response = requests.get('{}/{}'.format(API_URL, "RstEKey"), json = mes)
#print(response.json())

#Generate ephemeral keys
slist = []
Qlist = []
for i in range(0,10): #keeping the ID of the key as the index of the list
 s, Q = KeyGen()
 slist.append(s)
 Qlist.append(Q)
print("Ephemeral private keys are:",slist)
print("Ephemeral public keys are:", Qlist)

print("Signing and sending ephemeral keys...")
#sign ephemeral keys
for i in range(0,10):
  m = str(Qlist[i].x) + str(Qlist[i].y)
  h,s = SignGen(m, sL) #signing the message with long term private key
  ekey = Point(Qlist[i].x, Qlist[i].y,curve)

  #send ephemeral key
  mes = {'ID': stuID, 'KEYID': i , 'QAI.X': ekey.x, 'QAI.Y': ekey.y, 'Si': s, 'Hi': h}
  response = requests.put('{}/{}'.format(API_URL, "SendKey"), json = mes)
  print(response.json())


messagelist=[]
#sign student ID
for i in range(0,10): #getting all 10 messages (server is sending 10 messages although it is stated as 5 in the document)
  h, s = SignGen(stuID, sL)

  #Receiving Messages
  mes = {'ID_A': stuID, 'S': s, 'H': h}
  response = requests.get('{}/{}'.format(API_URL, "ReqMsg"), json = mes)
  print(response.json())
  messagelist.append(response.json())

print("Messsages are", messagelist)

print("Verifying and decrypting the messages...")
#decrypt messages
for j in range(0,10): #decrypting 10 messages
  i = int(messagelist[j]['KEYID']) #getting corresponding values from the dictionary
  QBJX = messagelist[j]['QBJ.X']
  QBJY = messagelist[j]['QBJ.Y']
  QBJ = Point(QBJX,QBJY,curve) #constructing the pointing
  ctext=messagelist[j]['MSG']

  ctext = ctext.to_bytes((ctext.bit_length()+7)//8, byteorder='big')
  T = slist[i]*QBJ
  U = str.encode(str(T.x) + str(T.y) + "NoNeedToRunAndHide")
  kenc = SHA3_256.new(U) #computing kenc
  kenc = kenc.digest()
  #print("kenc is", kenc)
  kmac = SHA3_256.new(kenc) #computing kmac
  kmac = kmac.digest()
  #print("kmac is",kmac)
  msg = ctext[8:len(ctext)- 32] #slicing the message
  #print("msg is", msg)
  mac = ctext[len(ctext)- 32:]
  #print("hmac is", mac)

  h = HMAC.new(kmac, digestmod=SHA256) #taken from https://pycryptodome.readthedocs.io/en/latest/src/hash/hmac.html and modified
  h.update(msg)
  try:
    #h.hexverify(mac)
    h.verify(mac)
    print("The message '%s' is authentic" % msg)
  except ValueError:
    print("The message or the key is wrong")

  ctext = ctext[:len(ctext)- 32]
  #print("ctext is", ctext)
  cipher = AES.new(kenc, AES.MODE_CTR,nonce=ctext[:8]) #AES decryption
  h = cipher.decrypt(ctext[8:]) 
  h = h.decode() 
  print("Decrypted message is", h)

  #send decrypted messages to server
  mes = {'ID_A': stuID, 'DECMSG': h}
  response = requests.put('{}/{}'.format(API_URL, "Checker"), json = mes)
  print(response.json())


'''
###delete ephemeral keys
mes = {'ID': stuID, 'S': s, 'H': h}
response = requests.get('{}/{}'.format(API_URL, "RstEKey"), json = mes)
'''

'''
###########DELETE LONG TERM KEY
# If you lost your long term key, you can reset it yourself with below code.

# First you need to send a request to delete it. 
mes = {'ID': stuID}
response = requests.get('{}/{}'.format(API_URL, "RstLongRqst"), json = mes)

#Then server will send a verification code to your email. 
# Send this code to server using below code
mes = {'ID': stuID, 'CODE' : code}
response = requests.get('{}/{}'.format(API_URL, "RstLong"), json = mes)

#Now your long term key is deleted. You can register again. 
'''

