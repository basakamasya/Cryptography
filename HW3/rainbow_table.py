# Do not forget to install pycryptodome if not already installed
# pip install pycryptodome

import random
from Crypto.Hash import SHA3_256
from Crypto import Random
import json

def Reduction(x, Alphabet, length):
  pwd = ""
  t = x
  size = len(Alphabet)
  for j in range(0,length):
    pwd += Alphabet[t%size]
    t = t//size
  return pwd  

Alphabet = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z', 26:'.', 27:',', 28:'!', 29:'?'}
alpha_len = len(Alphabet)
pwd_len = 6
pwd_space = alpha_len**pwd_len 
t = 2**16
m = 2*(pwd_space//t)
# Example for computing one link in the chain; i.e., pwd(i+1) = R(H(pwd(i)))
print("This is how you compute one link in the hash chain")
pwd_i = "OO,XR." # a sample password
hash = SHA3_256.new(pwd_i.encode('utf-8')) # hash it
digest = int.from_bytes(hash.digest(), byteorder='big') # convert the hash into an integer
pwd_i1 = Reduction(digest%pwd_space, Alphabet, pwd_len) # Reduce it
print("pwd(i) --> pwd(i+1): ", pwd_i, "-->",pwd_i1)
 
# Read the rainbow table
f = open("rainbowtable.txt","r")
Rainbow_Table = json.loads(f.read())
f.close()

# Check one link in the rainbow table
# Testing again
pwd = Rainbow_Table[2][0] # first password in the hash chain
for i in range(0, t):
  hash = SHA3_256.new(pwd.encode('utf-8')) # hash it
  digest = int.from_bytes(hash.digest(), byteorder='big') # convert the hash into an integer
  pwd = Reduction(digest%pwd_space, Alphabet, pwd_len) # Reduce it
if pwd == Rainbow_Table[2][1]:
  print("The test passed:)")
else:
  print("The test failed:(")

# Digests
digest = [0]*10
digest[0] = 111664175835087104818026813679238872718588809165046911779225699794856093318234
digest[1] = 22820135743409067449079360021966351594585914262162986849768422866228607661602
digest[2] = 108599214035190096488409120475956364703079898874019914677638880449026471756517
digest[3] = 21234386121809501770387358041573474064922612494850891675950061443379840969125
digest[4] = 42508126146154410056301808539858424271218053213640792882173505214611864544014
digest[5] = 64783167790903443741767010398218391243349287124874178051733305397541822733173
digest[6] = 82826180109313297280210926407782259750886481052153750677216672143209951974579
digest[7] = 33008806334497719733006758782270889566403799882342450961231531077463199594906
digest[8] = 17563120859203926938996769044422672255077260848700455621802133704969880909504
digest[9] = 60173057471840555660471689635731631341571403560184791576581681546926436200120

# Solution
for digest_i in digest:
  success = 0
  p_0 = Reduction(digest_i, Alphabet, pwd_len)
  for j in range(0, m):
    if p_0 == Rainbow_Table[j][1]:
      pwd = Rainbow_Table[j][0]
      for k in range(0, t-1):
        hash = SHA3_256.new(pwd.encode('utf-8'))
        pwd = Reduction(int.from_bytes(hash.digest(), byteorder='big'), Alphabet, pwd_len)
      hash = SHA3_256.new(pwd.encode('utf-8'))
      if int.from_bytes(hash.digest(), byteorder='big') == digest_i:
        print("Password iss: ", pwd, "i, j, k: ", 0, j, k)
        success = 1
        break

  if success == 0:
    p_i = p_0
    for i in range(1,t-1):
      hash = SHA3_256.new(p_i.encode('utf-8'))
      p_i = Reduction(int.from_bytes(hash.digest(), byteorder='big'), Alphabet, pwd_len)
      for j in range(0, m):
        if p_i == Rainbow_Table[j][1]:
          pwd = Rainbow_Table[j][0]
          for k in range(0, t-i):
            hash = SHA3_256.new(pwd.encode('utf-8'))
            digest = int.from_bytes(hash.digest(), byteorder='big')
            pwd = Reduction(digest, Alphabet, pwd_len)
            hash = SHA3_256.new(pwd.encode('utf-8'))
            if int.from_bytes(hash.digest(), byteorder='big') == digest_i:
              print("Password is: ", pwd, "i, j, k: ", i, j, k)
              success = 1
              break
        if success == 1:
          break
      if success == 1:
        break
