import math
import random
import warnings
import sympy

def phi(n):
    amount = 0
    for k in range(1, n + 1):
        if math.gcd(n, k) == 1:
            amount += 1
    return amount

def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a%b
    return a

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
      
small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,
                113]

def check_small_primes(p):
    for i in small_primes:
        if p%i==0:
            return -1
    return 1
    
def random_prime(lower_bound, upper_bound):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        p = random.randrange(lower_bound, upper_bound)
        if p < 10000:
            chck = sympy.isprime(p)    
        elif check_small_primes(p) == 1:
            chck = sympy.isprime(p)
    warnings.simplefilter('default')    
    return p


# Example usage
'''
p = random_prime(2**128)
q = random_prime(2**128)
n = p*q
phi_n = (p-1)*(q-1)

e = 67
d = modinv(e,phi_n)

m = b'my top secret key!!!???????....?'
print("m: ", m, len(m))

c = pow(int.from_bytes(m, byteorder='big'), e, n)

m_ = pow(c, d, n)

print(m_.to_bytes((m_.bit_length() + 7) // 8, byteorder='big'))
'''

#Question 3

import math
import random
import warnings
import sympy

def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a%b
    return a

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

def Solve(a,b,n):
  d = gcd(a,n)
  if d == 1:
    a_inv = modinv(a,n)
    sol = (b * a_inv) % n
    print(sol)
  elif b % d == 0:
      new_n = n / d
      new_b = b / d
      new_a = a / d
      a_tilda_inv = modinv(new_a,new_n)
      x_tilda = (a_tilda_inv * new_b) % new_n
      sol = []
      for i in range(d):
        sol.append(x_tilda + i * new_n)
        print(sol)
  else:
    print("NO SOLUTION")


n1 = 97289040915427312142046186233204893375
a1 = 61459853434867593821323745103091100940
b1 = 22119567361435062372463814709890918083
Solve(a1,b1,n1)

n2 = 97289040915427312142046186233204893375
a2 = 87467942514366097632147785951765210855
b2 = 3291682454206668645932879948693825640
Solve(a2,b2,n2)

n3 = 97289040915427312142046186233204893375
a3 = 74945727802091171826938590498744274413
b3 = 54949907590247169540755431623509626593
Solve(a3,b3,n3)