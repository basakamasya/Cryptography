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



PIN_ = 7146
########

# Client sends PIN_ to server
endpoint = '{}/{}/{}/{}'.format(API_URL, "RSA_OAEP", my_id, PIN_)
response = requests.put(endpoint)
print(response.json())
