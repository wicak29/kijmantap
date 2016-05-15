__author__ = 'Indra Gunawan'

from fractions import gcd

#lol = gcd(7,20)
#print lol

simpan =[]

def coprime (y):
    #simpan =[]
    for index in range(2,y):
        if gcd(index,y) == 1:
            hasil = gcd(index,y)
            simpan.append(index)
            index=+1

coprime(20)
print simpan
