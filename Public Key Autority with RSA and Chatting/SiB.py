__author__ = 'Indra Gunawan'
#client
import socket
import threading
from suds.client import Client

SIZE =4

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
    #return decMsg
    return decString

minPrime = 2
maxPrime = 100

#Generate P and Q value
cached_primes = [i for i in range(minPrime,maxPrime) if isPrime(i)]
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

ID = "Alice"

#request = idA+">"+idb+">"+Nance1
request = "first"+">"+ID

client = Client('http://10.151.43.106:8888/certificate/soap/description')
#client2 = Client('http://10.151.43.169:8888/KDC/soap/description')

publicKeyAuthReq = client.service.requestawal(request)
#print publicKeyAuth
publicKeyAuth = publicKeyAuthReq.split('>')
print "ouououo"
print publicKeyAuth[0]
print publicKeyAuth[1]


publicKeyA = str(publicKeyE)+'>'+str(N_Value)
Certificate = client.service.request(publicKeyA)

class client(threading.Thread):
    def __init__(self,c):
        threading.Thread.__init__(self)
        self.conn = c
        self.stopIt = False

    def mrecv(self):
        data = self.conn.recv(SIZE)
        self.conn.send('OK')
        return self.conn.recv(int(data))

    def run(self):
        while not self.stopIt:
            msg = self.mrecv()
            print 'recieved-> ',msg

soc1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc1.connect(('127.0.0.1',5432))
soc1.send('WILL SEND') # telling server we will send data from here

soc2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc2.connect(('127.0.0.1',5432))
soc2.send('WILL RECV') # telling server we will recieve data from here

def msend(conn,msg):
    if len(msg)<=999 and len(msg)>0:
        conn.send(str(len(msg)))
        if conn.recv(2) == 'OK':
            conn.send(msg)
    else:
        conn.send(str(999))
        if conn.recv(2) == 'OK':
            conn.send(msg[:999])
            msend(conn,msg[1000:]) # calling recursive
thr = client(soc2)
thr.start()
try:
    while 1:
        msend(soc1,raw_input())
except:
    print 'closing'
thr.stopIt=True
msend(soc1,'bye!!') # for stoping the thread
thr.conn.close()
soc1.close()
soc2.close()