__author__ = 'Indra Gunawan'
__author__ = 'Dwi Pratama'
__author__ = 'Adi Wicaksana'

import random, math
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

def intcaststr(bitlist):
    return int("".join(str(i) for i in bitlist), 2)

def bitfield(n):
    return [1 if digit=='1' else 0 for digit in bin(n)[2:]]

def str_ke_bitlist(s):
    ords = (ord(c) for c in s)
    shifts = (7, 6, 5, 4, 3, 2, 1, 0)
    return [(o >> shift) & 1 for o in ords for shift in shifts]

def bitlist_ke_chars(bl):
    bi = iter(bl)
    bytes = zip(*(bi,) * 8)
    shifts = (7, 6, 5, 4, 3, 2, 1, 0)
    for byte in bytes:
        yield chr(sum(bit << s for bit, s in zip(byte, shifts)))

def bitlist_ke_str(bl):
    return ''.join(bitlist_ke_chars(bl))

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

# Mengenkripsi kalimat
def encMessage(v_msg, v_e, v_n):
    encMsg = []
    for m in v_msg:
        print "Huruf : ", m
        c = (m ** v_e) % v_n
        print c
        encMsg.append(c)
    return encMsg

# Fungsi Dekripsi
def decMessage(v_msg, v_d, v_n):
    decMsg = []
    decString = ''
    for m in v_msg:
        print "Encript : ", m
        dec = (m ** v_d) % v_n
        print "Dec : ", dec
        strDec = chr(dec)
        decString+=strDec
        # print strDec
        decMsg.append(dec)
    print "Result : ", decString
    return decMsg

minPrime = 2
maxPrime = 100

#Generate P and Q value
cached_primes = [i for i in range(minPrime,maxPrime) if isPrime(i)]
# print "Cached : ", cached_primes
# P_Value = random.choice([i for i in cached_primes if minPrime < i < maxPrime])
# Q_Value = random.choice([i for i in cached_primes if minPrime < i < maxPrime])
# print "PQ : ", P_Value, Q_Value
P_Value = random.choice(cached_primes)
Q_Value = random.choice(cached_primes)
print "P : ", P_Value
print "Q : ", Q_Value

#Find N Value
N_Value = P_Value * Q_Value
print "N : ", N_Value

#Find Euler Totient
euler_totient = (P_Value-1)*(Q_Value-1)
print "Euler : ", euler_totient

#coprime(euler_totient, N_Value)
privateKeyD, publicKeyE = coprime(euler_totient, N_Value)
print "Private D : ", privateKeyD
print "Public E : ", publicKeyE

#==========Message conversion====
hel = "Hi! melody salsabila?"
# test = "abcd"
# hel2 = str_ke_bitlist(hel)
# print "H2 : ", hel2
# hel3 = intcaststr(hel2)
# print "H3 : ", hel3
# m = hel3

msg = [ord(c) for c in hel]
print "ASCII : ", msg


test = encMessage(msg, publicKeyE, N_Value)
print test
hasil = decMessage(test, privateKeyD, N_Value)
print hasil
# c = (m**publicKeyE)%N_Value
# print c
# decript = (c**privateKeyD)%N_Value
# print decript
# print chr(decript)

# hel4 = bitfield(decript)
# hel5 = bitlist_ke_str(hel4)

#print hel5

# print m
# print N_Value

#print P_Value
#print Q_Value
#print "p*q = "+ str(N_Value)
#print "euler totient = "+ str(euler_totient)
#print "show coprime = ", simpanCoprime
#print "Private key D = ", privateKeyD
#print "Public key E  = ", publicKeyE
#print "show biggest factor = " + str(biggestFactor)
