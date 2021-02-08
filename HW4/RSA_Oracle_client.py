import random
import requests

API_URL = 'http://cryptlygos.pythonanywhere.com'

my_id = 26628   ## Change this to your ID

endpoint = '{}/{}/{}'.format(API_URL, "RSA_Oracle", my_id )
response = requests.get(endpoint) 	
c, N, e = 0,0,0 
if response.ok:	
  res = response.json()
  print(res)
  c, N, e = res['c'], res['N'], res['e']    #get c, N, e
else: print(response.json())

######

c_ = 1

###### Query Oracle it will return corresponding plaintext
endpoint = '{}/{}/{}/{}'.format(API_URL, "RSA_Oracle_query", my_id, c_)
response = requests.get(endpoint) 	
if(response.ok): m_ = (response.json()['m_'])
else:print(response)

####

res = 609582572245086581955173486556226059889437853770629680858438291721089382181432413886171267314993856833992501

###Send your answer to the server.
endpoint = '{}/{}/{}/{}'.format(API_URL, "RSA_Oracle_checker", my_id, res)
response = requests.put(endpoint)
print(response.json())