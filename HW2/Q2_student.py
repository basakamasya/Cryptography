import requests

API_URL = 'http://cryptlygos.pythonanywhere.com'

my_id = 26628

endpoint = '{}/{}/{}'.format(API_URL, "q2", my_id )
response = requests.get(endpoint) 	
if response.ok:	
  r = response.json()
  p, q, e, c = r['p'], r['q'], r['e'], r['cipher']    #Use these variables to calculate m
  print(c)
else:  print(response.json())

##SOLUTION

n = p * q
phi_of_n = (p-1) * (q-1) #calculating phi of n
print("n is:", n)
print("phi(n) is:", phi_of_n)

#taken from helper code
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

d = modinv(e,phi_of_n) #calculating e inverse modula phi of n
print("d is:", d)
m = pow(c, d, n) #using power function of python because numbers are so big
print("m is:", m)

m_size = (m.bit_length() + 7 )//8 #converting bit length to byte length by dividing it by 8 (+ 7 for taking the ceiling of the division)
m_bytes = m.to_bytes(m_size,'big')
print("m in bytes form is:", m_bytes)
m_ = m_bytes.decode('utf-8') #decoding to utf-8 encoding
print("m in unicode string is:", m_)

## END OF SOLUTION

m = 4839340329840107805222872935385467764882532163271036774282858961177048507171921646440922047159462613679079365432800453808257350313247955215351159251488130043311177118337408029549590458606881358154284461926714643915353504702419793280055949859784310573460927866605146209780549162693493468729476945105120408793	#ATTN: change this into the number you calculated and DECODE it into a string m_
m_ = "Your secret number is 779"


#query result
endpoint = '{}/{}/{}/{}'.format(API_URL, "q2c", my_id, m_ )    #send your answer as a string
response = requests.put(endpoint) 	
print(response.json())
