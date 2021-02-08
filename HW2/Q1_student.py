import random
import requests

API_URL = 'http://cryptlygos.pythonanywhere.com' #DON'T Change this
my_id = 26628   # CHANGE this into your ID number

#server communication. Try to get p and t
endpoint = '{}/{}/{}'.format(API_URL, "q1", my_id )
response = requests.get(endpoint) 	
p = 0
t = 0
if response.ok:	
  res = response.json()
  print(res)
  p, t = res['p'], res['t']		#p is your prime number. t is the order of a subgroup. USE THESE TO SOLVE THE QUESTION
else:
  print(response.json())

##SOLUTION
#Question 1 - part a

#taken from helper code
small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,
                113]

def check_small_primes(p):
    for i in small_primes:
        if p%i==0:
            return -1
    return 1

if check_small_primes(823) == 1: #checking if 823 is prime
  print("Since 823 is a prime number, every integer greater than 0 and smaller than 823 is in Z823*.")
else:
  print("Not a prime. We should check for gcd's.")

Z823 = []
for i in range(1,823): #creating Z823*
  Z823.append(i)
print("Z823* is:", Z823)

answera = []
for j in range(0,822): #for each number in the group
  all_nums = Z823.copy() #getting a copy of the group list to work on
  for exp in range(1,823): #for each exponentiation
    num = (Z823[j]**exp) % 823
    if num in all_nums:
      all_nums.remove(num)
  if len(all_nums) == 0: #no number should be left in the list if Z823[j] generated all the numbers in the group
    #print(Gens)
    answera.append(Z823[j])
print("Generators of Z823* are:", answera)

#Question 1 - part b

answerb = []
for gh in range(2,823): #trying every number in subgroup
    num = pow(gh,137) #since this subgroup is cyclic, when the exponentiation is equal to the order, modulus 823 of it should be 1
    if num % 823 == 1:
      answerb.append(gh)
print("Generators of subgroup of Z823* with order 137 are:", answerb)


##END OF SOLUTION

g = 3 		#ATTN: change this into generator you found
gH = 8   	#ATTN: change this into generator of the subgroup you found


#You can CHECK result of PART A here
endpoint = '{}/{}/{}/{}'.format(API_URL, "q1ac", my_id, g)
response = requests.put(endpoint) 	
print(response.json())


#You can CHECK result of PART B here
endpoint = '{}/{}/{}/{}'.format(API_URL, "q1bc", my_id, gH )	#gH is generator of your subgroup
response = requests.put(endpoint) 	#check result
print(response.json())
