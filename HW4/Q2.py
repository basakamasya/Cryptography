# -*- coding: utf-8 -*-
"""Q2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H_gUJvd21b6khHUpDiCPhQNE0aj0KMIn
"""

# use "pip install pyprimes" if pyprimes is not installed
# use "pip install pycryptodome" if pycryptodome is not installed
import math
import random
import sympy
import requests

API_URL = 'http://cryptlygos.pythonanywhere.com'

my_id = 26628   #Change this to your ID

endpoint = '{}/{}/{}'.format(API_URL, "RSA_OAEP", my_id )   
response = requests.get(endpoint) 	
c, N, e = 0,0,0 
if response.ok:	
  res = response.json()
  print(res)
  c, N, e = res['c'], res['N'], res['e']    ##get c, N, e
else: print(response.json())

########
from RSA_OAEP import RSA_OAEP_Enc as RSA_OAEP_Enc
#c = 42358561498469920008048589721646035409248809569087914979674222533781930125542
#N = 69867813688925700002209409028318798092274838076935938891526949762546628296441
#e = 65537
found = False
blen = 8 #R is an 8-bit unsigned integer

for pin in range(0,10000): #pin can be any value between 0000 and 9999
  for R in range(2**(blen-1), 2**blen): #R can be any random integer between 2**(k0-1) and 2**k0-1
    c_ = RSA_OAEP_Enc(pin, e, N, R) #computing the pin
    if (c_ == c): #check if it's same with the ciphertext
      print("R is", R)
      print("Pin is",pin)
      found = True
      break
  if found:
    break

PIN_ = 7146
########

# Client sends PIN_ to server
endpoint = '{}/{}/{}/{}'.format(API_URL, "RSA_OAEP", my_id, PIN_)
response = requests.put(endpoint)
print(response.json())