__author__ = 'Indra Gunawan'

#C:\Python27\python.exe C:\Python27\Scripts\ladon-2.7-ctl.py testserve certificateAuthority.py -p 8888
from ladon.compat import PORTABLE_STRING

from ladon.ladonizer import ladonize
import math
import re
import collections
from ladon.types.ladontype import LadonType
import string
import random


#-------------------------------- RSA START ---------------------------------------------------------------------

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
        #print "Huruf : ", m
        c = (m ** v_e) % v_n
        #print c
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
    #return decMsg
    return decString

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
#---------------------------------------------RSA END------------------------------------------------------------
#Inisiasi Message dan Key


#idA = "alice"
#idb = "bob"
#Nance1 = "1"
idA = "alice"
idB = ""
Nance1 = ""
key_B = "bobkey01"
key_A = "alicekey"
ID = ""
#bungkus =""
#sertifikat = encMessage(bungkus, privateKeyD, N_Value)

# a = (12**200)%7
# print a
# wow ="cuy"
# lol = encMessage(wow, privateKeyD, N_Value)
# print lol
deskey =""
class certificate(object):

    @ladonize(str, rtype=str)
    def requestawal(self, ifile):
        global ID, deskey
        print "request diterima"
        bagi = ifile.split('>')
        #print ifile
        if bagi[0]=="first":
            publicAuth = str(publicKeyE)+'>'+str(N_Value)
            ID = bagi[1]
            deskey = bagi[2]
            #print ID
            #print publicAuth
            return publicAuth

    @ladonize(str, rtype=str)
    def request(self, ofile):
        global ID, privateKeyD, N_Value, deskey
        print "request diterima"

        #print ofile
        #bagi = ofile.split('>')

        waktu = "31-5-2016"
        PUa = ofile
        #print ID
        #listkey = [random.choice(string.ascii_letters + string.digits) for n in xrange(8)]
        #deskey = "".join(listkey)
        bungkus = waktu+'#'+ID+'#'+PUa+'#'+deskey
        print bungkus
        msg = [ord(c) for c in bungkus]
        #print "ASCII : ", msg
        sertifikat = encMessage(msg, privateKeyD, N_Value)
        #print sertifikat
        sertifikatkirim = str(sertifikat)
        #print sertifikatkirim
        # idA = bagi[0]
        # idB = bagi[1]
        # Nance1 = bagi[2]

        #print idA
        #print idB
        #print Nance1
        #print bagi4

        # listkey = [random.choice(string.ascii_letters + string.digits) for n in xrange(8)]
        # randomsessionkey = "".join(listkey)
        #
        # kumpulB = randomsessionkey+"|"+idA
        # paketB = enkripsi(key_B,kumpulB)
        # kumpulA = randomsessionkey+">"+idA+">"+idB+">"+Nance1+"#"+paketB
        # paketA = enkripsi(key_A,kumpulA)
        # paketAA = str_ke_bitlist(paketA)
        # paketAAA = str(paketAA)
        #return paketA
        # print kumpulB
        # print paketB
        # print kumpulA
        # print paketA
        #print paketAA
        #print paketAAA
        #print "request dikirim"
        return sertifikatkirim

