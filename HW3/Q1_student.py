import random
import requests
import BitVector

API_URL = 'http://cryptlygos.pythonanywhere.com'	#DON'T CHANGE THIS
my_id = 26628   									#ATTN: Change this into your id number

endpoint = '{}/{}/{}'.format(API_URL, "poly", my_id )
response = requests.get(endpoint) 	
a = 0
b = 0
if response.ok:	
  res = response.json()
  print(res)
  a, b = res['a'], res['b']		#Binary polynomials a and b
else:
  print(response.json())

##SOLUTION  

a_bv = BitVector.BitVector(bitstring = '11011111')
b_bv = BitVector.BitVector(bitstring = '00011101')
poly = BitVector.BitVector(bitstring= '100011011')
c = a_bv.gf_multiply_modular(b_bv, poly, 8)
c = str(c)
print(c)

a_inverse = a_bv.gf_MI(poly, 8)
a_inverse = str(a_inverse)
print(a_inverse)

#You need to calculate c and a_inv
#c = a(x)*b(x)
#a_inv is inverse of a
c = "01110011"
a_inv = "01101011"

##END OF SOLUTION
 

#check result of part a
endpoint = '{}/{}/{}/{}'.format(API_URL, "mult", my_id, c)
response = requests.put(endpoint) 	
print(response.json())

#check result of part b
endpoint = '{}/{}/{}/{}'.format(API_URL, "inv", my_id, a_inv)
response = requests.put(endpoint) 	
print(response.json())
