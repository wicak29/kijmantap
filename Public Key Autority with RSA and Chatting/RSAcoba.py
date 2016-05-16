__author__ = 'Indra Gunawan'
__author__ = 'Dwi Pratama'

import random
from fractions import gcd

simpanCoprime =[]

MMI = lambda A, n,s=1,t=0,N=0: (n < 2 and t%N or MMI(n, A%n, t, s-A//n*t, N or n),-1)[n<1]

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

def coprime (EulerTotient, N):
    for index in range(2,EulerTotient):
        if gcd(index,N) == 1:
            hasil = gcd(index,N)
            simpanCoprime.append(index)
            index=+1

    #return "hai", 1
    for index in simpanCoprime:
        if MMI(index, EulerTotient) != -1:
          return MMI(index, EulerTotient), index

minPrime = 0
maxPrime = 1000

#Generate P and Q value
cached_primes = [i for i in range(minPrime,maxPrime) if isPrime(i)]
P_Value = random.choice([i for i in cached_primes if minPrime < i < maxPrime])
Q_Value = random.choice([i for i in cached_primes if minPrime < i < maxPrime])

#Find N Value
N_Value = P_Value * Q_Value

#Find Euler Totient
euler_totient = (P_Value-1)*(Q_Value-1)

#coprime(euler_totient, N_Value)
privateKeyD, publicKeyE = coprime(euler_totient, N_Value)


print P_Value
print Q_Value
print "p*q = "+ str(N_Value)
print "euler totient = "+ str(euler_totient)
#print "show coprime = ", simpanCoprime
print "Private key D = ", privateKeyD
print "Public key E  = ", publicKeyE
#print "show biggest factor = " + str(biggestFactor)
