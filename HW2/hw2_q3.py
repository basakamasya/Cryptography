# -*- coding: utf-8 -*-
"""hw2_q3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZYraeB57dJUnHzrZYMMcwU30J_lLRFZR
"""

#Question 3

#taken from helper code
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

#to solve the equation
def Solve(a,b,n):
  d = gcd(a,n)
  if d == 1: #one unique solution if a and n are relatively prime
    a_inv = modinv(a,n)
    sol = (b * a_inv) % n  
    print("There is one unique solution:", sol)
  elif (b % d) == 0: #d number of solutions if d divides b
      print("GCD of a and n is", d, "and d divides b (with no remainder)")
      new_n = n // d
      new_b = b // d
      new_a = a // d
      a_tilda_inv = modinv(new_a,new_n)
      x_tilda = (a_tilda_inv * new_b) % new_n #solution of the new equation
      sol = []
      for i in range(d): #adding new_n, d-1 times to the solution of the new equation
        sol.append(x_tilda + i * new_n)
      print("There are exactly", d, "solutions and they are:", sol)
  else: #no solutions exist for this equation if d does not divide b
    print("GCD of a and n is", d, "when d divides b remainder is", (b % d))
    print("NO SOLUTION")

n = 97289040915427312142046186233204893375

a1 = 61459853434867593821323745103091100940
b1 = 22119567361435062372463814709890918083
print("For part a:")
Solve(a1,b1,n)
print("\n")

a2 = 87467942514366097632147785951765210855 
b2 = 3291682454206668645932879948693825640
print("For part b:")  
Solve(a2,b2,n)
print("\n")

a3 = 74945727802091171826938590498744274413 
b3 = 54949907590247169540755431623509626593
print("For part c:")    
Solve(a3,b3,n)