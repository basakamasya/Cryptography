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
from Crypto.Hash import SHA3_256, SHA256, HMAC
import requests
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import random
import hashlib, hmac, binascii
import json

from Crypto.Hash import HMAC, SHA256

API_URL = 'http://cryptlygos.pythonanywhere.com'

stuID =  12345
stuID_B = 18007

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
#print("h is", h)
#print("s is", s)

####Register Long Term Key

#s, h = SignGen(str(stuID).encode(), curve, sCli_long) #using our SignGen function
#mes = {'ID':stuID, 'H': h, 'S': s, 'LKEY.X': QCli_long.x, 'LKEY.Y': QCli_long.y}
#response = requests.put('{}/{}'.format(API_URL, "RegLongRqst"), json = mes)
#print(response.json())

#code = int(input())

#mes = {'ID':stuID, 'CODE': code}
#response = requests.put('{}/{}'.format(API_URL, "RegLong"), json = mes)
#print(response.json())

#Check Status
mes = {'ID_A':stuID, 'H': h, 'S': s}
response = requests.get('{}/{}'.format(API_URL, "Status"), json = mes)
print("Status ", response.json())

response = str(response.json())
key_num = 10 - int(response.split(" ")[2]) #getting the number of keys need to be send from the response
unread_msg_num = int(response.split(" ")[-4]) #getting the number of unread messages

key_dict = {}
#key_dict = {0: [82259256408469813777799681543519538779941237478943236509502183290460773414619, 32155947803828431008887792730917309338153723547328672537127587834810237591094, 8762018120919137670746632548839450685545562035184336023557809101439233565673], 1: [89456131913230466656074806789331802846468288876751092858876290386844178044539, 52229251378829020875730717270305066110061031332304447611694887928316420555250, 44652292947307800960068069848660726619517590092239506666690518580407493865498], 2: [2223755464676896662331649936760946473725474251659214114615070064529957136247, 65717483709282804750258295960938300423057002810035850984818589464170828888049, 115503133220853569224889683356438143237975691755661011681790744939053396722557], 3: [113242250209959051593668691443676236296364899336773258687379188228573477437749, 97747804544728033944217104143793441346701661017245601640512074397034237577854, 25281722312297563187955286920014129744996650090678508022909817396045007994338], 4: [66200359826588734986533216564108732385993975442889298384786901641661006143507, 73902557365691565207390839054085719954942890412162553361474840616472355266919, 112669851408150941627517111174456585541462585843896022754169075610711793862886], 5: [17123400920193592240558334056714866365950178751719541018658914081938133791724, 79469117869261432814011505421570496971008533083137314118416554574819407377227, 82170245666488815473787025904809657990078245157212886479902486162175464938561], 6: [74991801152866040162235194446502178207227470875617914124660056362340678058586, 104768515754237713248127281047945034707080613849070440655641191634446388072641, 17644884053873057103362300807712773493688118468925336899902053596902303295160], 7: [28557241315904877415198722195668400674434249685907819163320939363097204226631, 60722703226828432637778606589467077623606606035642074455840262593129555743670, 85302536391860221564519569208422606799772435891086087776279509455299935224650], 8: [65890752055611859897408622769414029326393435227195390129779073970260191954745, 30855917836828780468541279749506261296286282870116103850190874388120786425012, 85218792193359487829587943634798452223156266961498822140111408755893143204156], 9: [45620507570375013050431780348896452888357334901913428912876904421695483081055, 83650549082797217305253440448109596849263399951913248913531566936894080303517, 25057612231701742699821485486306889375380164353683061080955409288368213075308], 10: [6322499921786390247868266489782302094427875734392861019835407874492421073312, 99541340173144658298119049293605475674862808914482813906190440358885685407507, 80708578999970630775001453878705413568961039421010125691295578933524724034282], 11: [69318541183756169987457894072348982949707052706667182268773593767385286105160, 102624589768793274730724415271335612031086952799274326139478626165800688278108, 102584778527145488039732827264421455482137510850194174198581021361568524134338]}
#Generate ephemeral keys
for j in range(0,key_num):
  i = len(key_dict) #ID of the new key
  #print(i)
  s, Q = KeyGen()
  keys = [s,Q.x,Q.y]
  key_dict[i] = keys #adding the new key to the dictionary
  m = str(Q.x) + str(Q.y)
  h,s = SignGen(m, sL) #signing the message with long term private key
  ekey = Point(Q.x, Q.y,curve)
  #Send Ephemeral keys
  mes = {'ID': stuID, 'KEYID': i , 'QAI.X': ekey.x, 'QAI.Y': ekey.y, 'Si': s, 'Hi': h}
  response = requests.put('{}/{}'.format(API_URL, "SendKey"), json = mes)
  print(response.json())

print("Keys are:", key_dict)

h, s = SignGen(stuID_B,sL) #to get the ephemeral key of the receiver
### Get key of the Student B
mes = {'ID_A': stuID, 'ID_B':stuID_B, 'S': s, 'H': h}
response = requests.get('{}/{}'.format(API_URL, "ReqKey"), json = mes)
res = response.json()
print(res)
try:
  QBJX = res['QBJ.x']
  QBJY = res['QBJ.y']
  QBJ = Point(QBJX,QBJY,curve) #constructing the pointing
  i = int(res['i']) #my ephemeral key ID
  j = res['j']  #receiver's ephemeral key ID

  T = key_dict[i][0]*QBJ
  U = str.encode(str(T.x) + str(T.y) + "NoNeedToRunAndHide")
  kenc = SHA3_256.new(U) #computing kenc
  kenc = kenc.digest()
  #print("kenc is", kenc)
  kmac = SHA3_256.new(kenc) #computing kmac
  kmac = kmac.digest()
  ptext = "The world is full of lonely people afraid to make the first move. Tony Lip"
  #ptext = "I don't like sand. It's all coarse, and rough, and irritating. And it gets everywhere. Anakin Skywalker"
  #ptext = "Hate is baggage. Life's too short to be pissed of all the time. It's just not worth it. Danny Vinyard"
  #ptext = "Well, sir, it's this rug I have, it really tied the room together. The Dude"
  #ptext = "Love is like taking a dump, Butters. Sometimes it works itself out. But sometimes, you need to give it a nice hard slimy push. Eric Theodore Cartman"
  print("Sending the message:", ptext)

  cipher = AES.new(kenc, AES.MODE_CTR) #using kenc as key of the AES
  ctext = cipher.encrypt(str.encode(ptext))

  h = HMAC.new(kmac, digestmod=SHA256)
  h.update(ctext)
  h = h.digest()
  msg = cipher.nonce + ctext + h
  msg = int.from_bytes(msg, byteorder='big')

  ### Send message to student B
  mes = {'ID_A': stuID, 'ID_B':stuID_B, 'I': i, 'J':j, 'MSG': msg}
  print(mes)
  response = requests.put('{}/{}'.format(API_URL, "SendMsg"), json = mes)
  print(response.json())

except TypeError:
  print("Message cannot be send because receiver has no ephemeral key")

## Get your message
for x in range(unread_msg_num):
  h, s = SignGen(stuID,sL)
  mes = {'ID_A': stuID, 'S': s, 'H': h}
  response = requests.get('{}/{}'.format(API_URL, "ReqMsg_PH3"), json = mes)
  print(response.json())
  if (response.ok) and response.json() != "You dont have any new messages": ## Decrypt message
    response = response.json()
    ctext = response['MSG']
    ctext = ctext.to_bytes((ctext.bit_length()+7)//8, byteorder='big')
    i = int(response['KEYID']) #getting corresponding values from the dictionary
    QBJX = response['QBJ.X']
    QBJY = response['QBJ.Y']
    QBJ = Point(QBJX,QBJY,curve) #constructing the pointing
    T = key_dict[i][0]*QBJ
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

    h = HMAC.new(kmac, digestmod=SHA256) #verifying the message
    h.update(msg)
    try:
      h.verify(mac)
      print("The message '%s' is authentic" % msg)
    except ValueError:
      print("The message or the key is wrong")

    ctext = ctext[:len(ctext)- 32]
    #print("ctext is", ctext)
    cipher = AES.new(kenc, AES.MODE_CTR,nonce=ctext[:8]) #AES decryption
    h = cipher.decrypt(ctext[8:]) 
    h = h.decode() 
    print("Decrypted message is:", h)

'''
#####Reset Ephemeral Keys
s, h = SignGen("18007".encode(), curve, sCli_long)
mes = {'ID': stuID, 'S': s, 'H': h}
print(mes)
response = requests.get('{}/{}'.format(API_URL, "RstEKey"), json = mes)
print(response.json())


#####Reset Long Term Key
mes = {'ID': stuID}
response = requests.get('{}/{}'.format(API_URL, "RstLongRqst"), json = mes)
print(response.json())
code = int(input())

mes = {'ID': stuID ,'CODE': code}
response = requests.get('{}/{}'.format(API_URL, "RstLong"), json = mes)
print(response.json())
'''