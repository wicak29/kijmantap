__author__ = 'Indra Gunawan'

import random
from fractions import gcd

def isPrime(n):
    """"pre-condition: n is a nonnegative integer
    post-condition: return True if n is prime and False otherwise."""
    if n < 2:
         return False;
    if n % 2 == 0:
         return n == 2  # return False
    k = 3
    while k*k <= n:
         if n % k == 0:
             return False
         k += 2
    return True

# def coprimes(num):
#     for x in range (2, num):
#         for y in range (2, num):
#             while (gcd(x,y) == 1) & (x != y):
#                 if (x*y==num):
#                     return (x,y)


minPrime = 0
maxPrime = 10
p = 0
q = 10

cached_primes = [i for i in range(minPrime,maxPrime) if isPrime(i)]
n1 = random.choice([i for i in cached_primes if p<i<q])
n2 = random.choice([i for i in cached_primes if p<i<q])

n = n1*n2
euler_totient = (n1-1)*(n2-1)

#lol = coprimes(20)
lol = gcd(20,8)
print n1
print n2
print n
print euler_totient
print lol
