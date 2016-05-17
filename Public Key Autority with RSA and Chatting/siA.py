__author__ = 'Indra Gunawan'
#server
import socket
import threading
import time
import random
import string
from suds.client import Client

#-------------------------------- DES START ---------------------------------------------------------------------
#Ubah string ke biner
def str_ke_bitlist(s):
    ords = (ord(c) for c in s)
    shifts = (7, 6, 5, 4, 3, 2, 1, 0)
    return [(o >> shift) & 1 for o in ords for shift in shifts]

#Ubah biner ke char
def bitlist_ke_chars(bl):
    bi = iter(bl)
    bytes = zip(*(bi,) * 8)
    shifts = (7, 6, 5, 4, 3, 2, 1, 0)
    for byte in bytes:
        yield chr(sum(bit << s for bit, s in zip(byte, shifts)))

#Dari biner ke string
def bitlist_ke_str(bl):
    return ''.join(bitlist_ke_chars(bl))

def enkripsi(kunci, pesan):
    mess = []
    mess_count = 0
    start = 0
    end = 8

    p_mess = len(pesan)
    index = p_mess

    while index > 0 :
        p_mess = len(pesan)
        if p_mess % end !=0:
            if p_mess < end :
                while p_mess<end:
                    pesan += '~'
                    p_mess = len(pesan)
        mess.append(pesan[start:end])
        mess_count += 1
        pesan = pesan[end:]
        # print pesan
        # print mess[mess_count]
        index -= end
        # print index
    # print mess

    def halfK(init, last, Kpermutate):

        H = [8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8]
        i = 0
        for x in range(init, last):
            H[i] = Kpermutate[x]
            i+=1
        return H

    def shift(l, n):
        return l[n:] + l[:n]

    def newKey(PC, C, D):
        CD = C
        CD.extend(D)
        nKey = [None]*48
        for x in range(0, len(PC)):
            a = PC[x]-1
            tempKey = CD[a]
            nKey[x] = tempKey
        return nKey


    def fungsi1(awal, tabel):
        hasilIP = [None]*64
        for x in range(0, len(tabel)):
            a= tabel[x]-1
            tempmessage = awal[a]
            hasilIP[x] = tempmessage
        return hasilIP

    def ulangR(key, left, right):

        Expand = [32,     1,    2,     3,     4,    5]
        Expand.extend( [4,     5,    6,     7,     8,    9] )
        Expand.extend([8,     9,   10,    11,    12,   13])
        Expand.extend([12,    13,   14,    15,    16,   17])
        Expand.extend([16,    17,   18,    19,    20,   21])
        Expand.extend([20,    21,   22,    23,    24,   25])
        Expand.extend([24,    25,   26,    27,    28,   29])
        Expand.extend([28,    29,   30,    31,    32,    1])


        right0 = [None]*48

        for x in range(0, len(Expand)):
            a= Expand[x]-1
            tempr = right[a]
            right0[x] = tempr

        #XOR fungsi K1+E(R0)
        fungsi = map(lambda x, y: x^y, key,right0 )

        sbox = [
                # S1
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
                 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
                 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
                 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

                # S2
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
                 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
                 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
                 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

                # S3
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
                 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
                 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
                 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

                # S4
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
                 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
                 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
                 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

                # S5
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
                 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
                 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
                 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

                # S6
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
                 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
                 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
                 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

                # S7
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
                 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
                 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
                 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

                # S8
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
                 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
                 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
                 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]

        B = [fungsi[:6], fungsi[6:12], fungsi[12:18], fungsi[18:24], fungsi[24:30], fungsi[30:36], fungsi[36:42], fungsi[42:]]

        j = 0
        Btot = [None] * 32
        pos = 0

        while j < 8:
            # cari nilai bit pertama dan keenam, cari nilai 4 bit ditengah
            m = (B[j][0] << 1) + B[j][5]
            n = (B[j][1] << 3) + (B[j][2] << 2) + (B[j][3] << 1) + B[j][4]
            # Menentukan nilai dari sbox
            v = sbox[j][(m << 4) + n]

            Btot[pos] = (v & 8) >> 3
            Btot[pos + 1] = (v & 4) >> 2
            Btot[pos + 2] = (v & 2) >> 1
            Btot[pos + 3] = v & 1

            pos += 4
            j += 1

        P = [16,   7,  20,  21]
        P.extend( [29,  12,  28,  17] )
        P.extend([ 1,  15,  23,  26])
        P.extend([ 5,  18,  31,  10])
        P.extend([2,   8,  24,  14])
        P.extend([32,  27,   3,   9])
        P.extend([19,  13,  30,   6])
        P.extend([22,  11,   4,  25])

        fungsicomplete = [None]*32

        for x in range(0, len(P)):
            a= P[x]-1
            #print a
            tempf = Btot[a]
            #print tempKey
            fungsicomplete[x] = tempf
            #print key[a]

        #print fungsicomplete
        newright = map(lambda x, y: x^y, left,fungsicomplete )
        return newright


    b_key = str_ke_bitlist(kunci)
    key = b_key
    PC1 = [57,  49,    41,   33,    25,    17,    9]
    PC1.extend( [1,   58,   50,   42,   34,   26,   18] )
    PC1.extend([10,    2,    59,   51,    43,    35,   27])
    PC1.extend([19,   11,     3,   60,    52,    44,   36])
    PC1.extend([63,   55,    47,   39,    31,    23,   15])
    PC1.extend([7,   62,    54,   46,    38,    30,   22])
    PC1.extend([14,    6,    61,   53,    45,    37,   29])
    PC1.extend([21,   13,     5,   28,    20,    12,    4])

    #Kp = [8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8]
    Kp = [None] * 56
        #Kp[0] = 999

    for x in range(0, len(PC1)):
        a = PC1[x]-1
        tempKey = key[a]
        Kp[x] = tempKey

    #print Kp
    C0 = halfK(0, (len(Kp)/2), Kp)
    #print C0
    D0 = halfK((len(Kp)/2), len(Kp), Kp)
    #print D0

    leftShift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2 ,1]

    C1 = shift(C0, leftShift[0])
    D1 = shift(D0, leftShift[0])

    C2 = shift(C1, leftShift[1])
    D2 = shift(D1, leftShift[1])

    C3 = shift(C2, leftShift[2])
    D3 = shift(D2, leftShift[2])

    C4 = shift(C3, leftShift[3])
    D4 = shift(D3, leftShift[3])

    C5 = shift(C4, leftShift[4])
    D5 = shift(D4, leftShift[4])

    C6 = shift(C5, leftShift[5])
    D6 = shift(D5, leftShift[5])

    C7 = shift(C6, leftShift[6])
    D7 = shift(D6, leftShift[6])

    C8 = shift(C7, leftShift[7])
    D8 = shift(D7, leftShift[7])

    C9 = shift(C8, leftShift[8])
    D9 = shift(D8, leftShift[8])

    C10 = shift(C9, leftShift[9])
    D10 = shift(D9, leftShift[9])

    C11 = shift(C10, leftShift[10])
    D11 = shift(D10, leftShift[10])

    C12 = shift(C11, leftShift[11])
    D12 = shift(D11, leftShift[11])

    C13 = shift(C12, leftShift[12])
    D13 = shift(D12, leftShift[12])

    C14 = shift(C13, leftShift[13])
    D14 = shift(D13, leftShift[13])

    C15 = shift(C14, leftShift[14])
    D15 = shift(D14, leftShift[14])

    C16 = shift(C15, leftShift[15])
    D16 = shift(D15, leftShift[15])

    #PC2
    PC2 = [14,    17,   11,    24,     1,    5]
    PC2.extend([3,   28,   15,     6,    21,   10])
    PC2.extend([23,   19,   12,     4,    26,    8])
    PC2.extend([16,   7,   27,    20,    13,    2])
    PC2.extend([41,    52,   31,    37,    47,   55])
    PC2.extend([30,   40,   51,    45,    33,   48])
    PC2.extend([44,    49,   39,    56,    34,   53])
    PC2.extend([46,    42,   50,    36,    29,   32])

    K1 = newKey(PC2, C1, D1)
    K2 = newKey(PC2, C2, D2)
    K3 = newKey(PC2, C3, D3)
    K4 = newKey(PC2, C4, D4)
    K5 = newKey(PC2, C5, D5)
    K6 = newKey(PC2, C6, D6)
    K7 = newKey(PC2, C7, D7)
    K8 = newKey(PC2, C8, D8)
    K9 = newKey(PC2, C9, D9)
    K10 = newKey(PC2, C10, D10)
    K11 = newKey(PC2, C11, D11)
    K12 = newKey(PC2, C12, D12)
    K13 = newKey(PC2, C13, D13)
    K14 = newKey(PC2, C14, D14)
    K15 = newKey(PC2, C15, D15)
    K16 = newKey(PC2, C16, D16)


    IP = [58,    50,   42,    34,    26,   18,    10,    2]
    IP.extend( [60,    52,   44,    36,    28,   20,    12,    4] )
    IP.extend([62,    54,   46,    38,    30,   22,    14,    6])
    IP.extend([64,    56,   48,    40,    32,   24,    16,    8])
    IP.extend([57,    49,   41,    33,    25,   17,     9,    1])
    IP.extend([59,    51,   43,    35,    27,   19,    11,    3])
    IP.extend([61,    53,   45,    37,    29,   21,    13,    5])
    IP.extend([63,    55,   47,    39,    31,   23,    15,    7])

    IPR = [
        40, 8,  48, 16, 56, 24, 64, 32,
        39, 7,  47, 15, 55, 23, 63, 31,
        38, 6,  46, 14, 54, 22, 62, 30,
        37, 5,  45, 13, 53, 21, 61, 29,
        36, 4,  44, 12, 52, 20, 60, 28,
        35, 3,  43, 11, 51, 19, 59, 27,
        34, 2,  42, 10, 50, 18, 58, 26,
        33, 1,  41, 9,  49, 17, 57, 25
    ]

    def f_enkripsi(msg):
        message = str_ke_bitlist(msg)

        #print hasilIP
        resultIP = fungsi1(message, IP)
        leftM = resultIP[:len(resultIP)/2]
        rightM = resultIP[len(resultIP)/2:]

        left1 = rightM
        right1 = ulangR(K1, leftM, rightM)

        left2 = right1
        right2 = ulangR(K2, left1, right1)

        left3 = right2
        right3 = ulangR(K3, left2, right2)

        left4 = right3
        right4 = ulangR(K4, left3, right3)

        left5 = right4
        right5 = ulangR(K5, left4, right4)

        left6 = right5
        right6 = ulangR(K6, left5, right5)

        left7 = right6
        right7 = ulangR(K7, left6, right6)

        left8 = right7
        right8 = ulangR(K8, left7, right7)

        left9 = right8
        right9 = ulangR(K9, left8, right8)

        left10 = right9
        right10 = ulangR(K10, left9, right9)

        left11 = right10
        right11 = ulangR(K11, left10, right10)

        left12 = right11
        right12 = ulangR(K12, left11, right11)

        left13 = right12
        right13 = ulangR(K13, left12, right12)

        left14 = right13
        right14 = ulangR(K14, left13, right13)

        left15 = right14
        right15 = ulangR(K15, left14, right14)

        left16 = right15
        right16 = ulangR(K16, left15, right15)

        final = left16
        final.extend(right16)
        finalIP = [None]*64

        for x in range(0, len(IPR)):
            a= IPR[x]-1
            tempf = final[a]
            #print tempKey
            finalIP[x] = tempf
            #print key[a]

        #print "IP-1 : ", finalIP
        #print len(finalIP)
        #print bitlist_ke_str(finalIP)
        return bitlist_ke_str(finalIP)

    finalEnkrip = ''
    #finalDekrip = ''
    for index in range(0, len(mess)):
        hasilenkripsi = f_enkripsi(mess[index])
        #hasildekripsi = f_dekripsi(hasilenkripsi)
        finalEnkrip = finalEnkrip + hasilenkripsi
        #finalDekrip = finalDekrip + hasildekripsi

    #print "DES : ", finalEnkrip
    return finalEnkrip
    #print "Decrypt : ", finalDekrip
#--------------------------------------------END DES ----------------------------------------------------------------
#-------------------------------------------BEGIN DECRYPT------------------------------------------------------------
def dekripsi(kunci, pesan):
    mess = []
    mess_count = 0
    start = 0
    end = 8

    p_mess = len(pesan)
    index = p_mess

    while index > 0 :
        p_mess = len(pesan)
        if p_mess % end !=0:
            if p_mess < end :
                while p_mess<end:
                    pesan += '-'
                    p_mess = len(pesan)
        mess.append(pesan[start:end])
        mess_count += 1
        pesan = pesan[end:]
        # print pesan
        # print mess[mess_count]
        index -= end
        # print index
    # print mess

    def halfK(init, last, Kpermutate):

        H = [8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8]
        i = 0
        for x in range(init, last):
            H[i] = Kpermutate[x]
            i+=1
        return H

    def shift(l, n):
        return l[n:] + l[:n]

    def newKey(PC, C, D):
        CD = C
        CD.extend(D)
        nKey = [None]*48
        for x in range(0, len(PC)):
            a = PC[x]-1
            tempKey = CD[a]
            nKey[x] = tempKey
        return nKey


    def fungsi1(awal, tabel):
        hasilIP = [None]*64
        for x in range(0, len(tabel)):
            a= tabel[x]-1
            tempmessage = awal[a]
            hasilIP[x] = tempmessage
        return hasilIP

    def ulangR(key, left, right):

        Expand = [32,     1,    2,     3,     4,    5]
        Expand.extend( [4,     5,    6,     7,     8,    9] )
        Expand.extend([8,     9,   10,    11,    12,   13])
        Expand.extend([12,    13,   14,    15,    16,   17])
        Expand.extend([16,    17,   18,    19,    20,   21])
        Expand.extend([20,    21,   22,    23,    24,   25])
        Expand.extend([24,    25,   26,    27,    28,   29])
        Expand.extend([28,    29,   30,    31,    32,    1])


        right0 = [None]*48

        for x in range(0, len(Expand)):
            a= Expand[x]-1
            tempr = right[a]
            right0[x] = tempr

        #XOR fungsi K1+E(R0)
        fungsi = map(lambda x, y: x^y, key,right0 )

        sbox = [
                # S1
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
                 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
                 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
                 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

                # S2
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
                 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
                 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
                 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

                # S3
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
                 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
                 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
                 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

                # S4
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
                 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
                 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
                 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

                # S5
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
                 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
                 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
                 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

                # S6
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
                 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
                 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
                 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

                # S7
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
                 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
                 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
                 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

                # S8
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
                 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
                 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
                 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]

        B = [fungsi[:6], fungsi[6:12], fungsi[12:18], fungsi[18:24], fungsi[24:30], fungsi[30:36], fungsi[36:42], fungsi[42:]]

        j = 0
        Btot = [None] * 32
        pos = 0

        while j < 8:
            # cari nilai bit pertama dan keenam, cari nilai 4 bit ditengah
            m = (B[j][0] << 1) + B[j][5]
            n = (B[j][1] << 3) + (B[j][2] << 2) + (B[j][3] << 1) + B[j][4]
            # Menentukan nilai dari sbox
            v = sbox[j][(m << 4) + n]

            Btot[pos] = (v & 8) >> 3
            Btot[pos + 1] = (v & 4) >> 2
            Btot[pos + 2] = (v & 2) >> 1
            Btot[pos + 3] = v & 1

            pos += 4
            j += 1

        P = [16,   7,  20,  21]
        P.extend( [29,  12,  28,  17] )
        P.extend([ 1,  15,  23,  26])
        P.extend([ 5,  18,  31,  10])
        P.extend([2,   8,  24,  14])
        P.extend([32,  27,   3,   9])
        P.extend([19,  13,  30,   6])
        P.extend([22,  11,   4,  25])

        fungsicomplete = [None]*32

        for x in range(0, len(P)):
            a= P[x]-1
            #print a
            tempf = Btot[a]
            #print tempKey
            fungsicomplete[x] = tempf
            #print key[a]

        #print fungsicomplete
        newright = map(lambda x, y: x^y, left,fungsicomplete )
        return newright


    b_key = str_ke_bitlist(kunci)
    key = b_key
    PC1 = [57,  49,    41,   33,    25,    17,    9]
    PC1.extend( [1,   58,   50,   42,   34,   26,   18] )
    PC1.extend([10,    2,    59,   51,    43,    35,   27])
    PC1.extend([19,   11,     3,   60,    52,    44,   36])
    PC1.extend([63,   55,    47,   39,    31,    23,   15])
    PC1.extend([7,   62,    54,   46,    38,    30,   22])
    PC1.extend([14,    6,    61,   53,    45,    37,   29])
    PC1.extend([21,   13,     5,   28,    20,    12,    4])

    #Kp = [8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8]
    Kp = [None] * 56
        #Kp[0] = 999

    for x in range(0, len(PC1)):
        a = PC1[x]-1
        tempKey = key[a]
        Kp[x] = tempKey

    #print Kp
    C0 = halfK(0, (len(Kp)/2), Kp)
    #print C0
    D0 = halfK((len(Kp)/2), len(Kp), Kp)
    #print D0

    leftShift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2 ,1]

    C1 = shift(C0, leftShift[0])
    D1 = shift(D0, leftShift[0])

    C2 = shift(C1, leftShift[1])
    D2 = shift(D1, leftShift[1])

    C3 = shift(C2, leftShift[2])
    D3 = shift(D2, leftShift[2])

    C4 = shift(C3, leftShift[3])
    D4 = shift(D3, leftShift[3])

    C5 = shift(C4, leftShift[4])
    D5 = shift(D4, leftShift[4])

    C6 = shift(C5, leftShift[5])
    D6 = shift(D5, leftShift[5])

    C7 = shift(C6, leftShift[6])
    D7 = shift(D6, leftShift[6])

    C8 = shift(C7, leftShift[7])
    D8 = shift(D7, leftShift[7])

    C9 = shift(C8, leftShift[8])
    D9 = shift(D8, leftShift[8])

    C10 = shift(C9, leftShift[9])
    D10 = shift(D9, leftShift[9])

    C11 = shift(C10, leftShift[10])
    D11 = shift(D10, leftShift[10])

    C12 = shift(C11, leftShift[11])
    D12 = shift(D11, leftShift[11])

    C13 = shift(C12, leftShift[12])
    D13 = shift(D12, leftShift[12])

    C14 = shift(C13, leftShift[13])
    D14 = shift(D13, leftShift[13])

    C15 = shift(C14, leftShift[14])
    D15 = shift(D14, leftShift[14])

    C16 = shift(C15, leftShift[15])
    D16 = shift(D15, leftShift[15])

    #PC2
    PC2 = [14,    17,   11,    24,     1,    5]
    PC2.extend([3,   28,   15,     6,    21,   10])
    PC2.extend([23,   19,   12,     4,    26,    8])
    PC2.extend([16,   7,   27,    20,    13,    2])
    PC2.extend([41,    52,   31,    37,    47,   55])
    PC2.extend([30,   40,   51,    45,    33,   48])
    PC2.extend([44,    49,   39,    56,    34,   53])
    PC2.extend([46,    42,   50,    36,    29,   32])

    K1 = newKey(PC2, C1, D1)
    K2 = newKey(PC2, C2, D2)
    K3 = newKey(PC2, C3, D3)
    K4 = newKey(PC2, C4, D4)
    K5 = newKey(PC2, C5, D5)
    K6 = newKey(PC2, C6, D6)
    K7 = newKey(PC2, C7, D7)
    K8 = newKey(PC2, C8, D8)
    K9 = newKey(PC2, C9, D9)
    K10 = newKey(PC2, C10, D10)
    K11 = newKey(PC2, C11, D11)
    K12 = newKey(PC2, C12, D12)
    K13 = newKey(PC2, C13, D13)
    K14 = newKey(PC2, C14, D14)
    K15 = newKey(PC2, C15, D15)
    K16 = newKey(PC2, C16, D16)


    IP = [58,    50,   42,    34,    26,   18,    10,    2]
    IP.extend( [60,    52,   44,    36,    28,   20,    12,    4] )
    IP.extend([62,    54,   46,    38,    30,   22,    14,    6])
    IP.extend([64,    56,   48,    40,    32,   24,    16,    8])
    IP.extend([57,    49,   41,    33,    25,   17,     9,    1])
    IP.extend([59,    51,   43,    35,    27,   19,    11,    3])
    IP.extend([61,    53,   45,    37,    29,   21,    13,    5])
    IP.extend([63,    55,   47,    39,    31,   23,    15,    7])

    IPR = [
        40, 8,  48, 16, 56, 24, 64, 32,
        39, 7,  47, 15, 55, 23, 63, 31,
        38, 6,  46, 14, 54, 22, 62, 30,
        37, 5,  45, 13, 53, 21, 61, 29,
        36, 4,  44, 12, 52, 20, 60, 28,
        35, 3,  43, 11, 51, 19, 59, 27,
        34, 2,  42, 10, 50, 18, 58, 26,
        33, 1,  41, 9,  49, 17, 57, 25
    ]

    def f_dekripsi (hasilenkripsi):
        hasil = str_ke_bitlist(hasilenkripsi)
        CC = fungsi1(hasil, IP)
        #print CC

        RR0 = CC[:len(CC)/2]
        LL0 = CC[len(CC)/2:]

        LL1 = RR0
        RR1 = ulangR(K16, LL0, RR0)

        LL2 = RR1
        RR2 = ulangR(K15, LL1, RR1)

        LL3 = RR2
        RR3 = ulangR(K14, LL2, RR2)

        LL4 = RR3
        RR4 = ulangR(K13, LL3, RR3)

        LL5 = RR4
        RR5 = ulangR(K12, LL4, RR4)

        LL6 = RR5
        RR6 = ulangR(K11, LL5, RR5)

        LL7 = RR6
        RR7 = ulangR(K10, LL6, RR6)

        LL8 = RR7
        RR8 = ulangR(K9, LL7, RR7)

        LL9 = RR8
        RR9 = ulangR(K8, LL8, RR8)

        LL10 = RR9
        RR10 = ulangR(K7, LL9, RR9)

        LL11 = RR10
        RR11 = ulangR(K6, LL10, RR10)

        LL12 = RR11
        RR12 = ulangR(K5, LL11, RR11)

        LL13 = RR12
        RR13 = ulangR(K4, LL12, RR12)

        LL14 = RR13
        RR14 = ulangR(K3, LL13, RR13)

        LL15 = RR14
        RR15 = ulangR(K2, LL14, RR14)

        LL16 = RR15
        RR16 = ulangR(K1, LL15, RR15)

        TTinv = RR16
        TTinv.extend(LL16)

        TT = fungsi1(TTinv, IPR)

        #print message
        #print TT

        return bitlist_ke_str(TT)

    #finalEnkrip = ''
    finalDekrip = ''
    for index in range(0, len(mess)):
        #hasilenkripsi = f_enkripsi()
        hasildekripsi = f_dekripsi(mess[index])
        #finalEnkrip = finalEnkrip + hasilenkripsi
        finalDekrip = finalDekrip + hasildekripsi

    #print "DES : ", finalEnkrip
    #print "Decrypt : ", finalDekrip
    return finalDekrip


#---------------------------------------------END DECRYPT------------------------------------------------------------



SIZE = 4

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
        #print "Encript : ", m
        dec = (m ** v_d) % v_n
        #print "Dec : ", dec
        strDec = chr(dec)
        decString+=strDec
        # print strDec
        decMsg.append(dec)
    #print "Result : ", decString
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
#---------------------------------------Generate Key DES---------------------------------------------------------
listkey = [random.choice(string.ascii_letters + string.digits) for n in xrange(8)]
Mydeskey = "".join(listkey)
#--------------------------------------------Genereate END-------------------------------------------------------

ID = "Alice"
waktu = ""
IDteman = ""
PUteman = 0
Nteman = 0
deskeyteman = ""
#request = idA+">"+idb+">"+Nance1
request = "first"+">"+ID+">"+Mydeskey

client = Client('http://10.151.43.122:8888/certificate/soap/description')
#client2 = Client('http://10.151.43.169:8888/KDC/soap/description')

publicKeyAuthReq = client.service.requestawal(request)
#print publicKeyAuth
publicKeyAuth = publicKeyAuthReq.split('>')

print "Public key pow : ", publicKeyAuth[0]
print "Public key mod : ", publicKeyAuth[1]
#print "My Des key : ", publicKeyAuth[2]
print Mydeskey


publicKeyA = str(publicKeyE)+'>'+str(N_Value)
CertificateA = client.service.request(publicKeyA)
CertificateB = ""
print CertificateA

#split certificate

certSplit = CertificateA.split("[")
certSplit2 = certSplit[1].split("]")
certSplit3 = certSplit2[0].split(", ")
temp = map(lambda each:each.strip("L"), certSplit3)

temp2 = [int(i) for i in temp]
print temp2
#print temp2[0]

decCert = decMessage(temp2, int(publicKeyAuth[0]), int(publicKeyAuth[1]))
print "hasil decrypt = ", decCert

soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.bind(('127.0.0.1',5432))
soc.listen(5)

class CThread(threading.Thread):
    def __init__(self,c):
        threading.Thread.__init__(self)
        self.conn = c
        self.stopIt=False

    def mrecv(self):
        data = self.conn.recv(SIZE)
        self.conn.send('OK')
        msg = self.conn.recv(int(data))
        return msg

    def run(self):
        global CertificateB, waktu, IDteman, PUteman, Nteman, deskeyteman
        while not self.stopIt:
            msg = self.mrecv()
            if msg[0]=="[":
                CertificateB = msg
                print "Dapat Certificate ->", CertificateB
                certSplit = CertificateB.split("[")
                certSplit2 = certSplit[1].split("]")
                certSplit3 = certSplit2[0].split(", ")
                temp = map(lambda each:each.strip("L"), certSplit3)

                temp2 = [int(i) for i in temp]

                decCert = decMessage(temp2, int(publicKeyAuth[0]), int(publicKeyAuth[1]))
                print "hasil decrypt = ", decCert
                hasilbagi=decCert.split("#")
                print hasilbagi
                waktu = hasilbagi[0]
                IDteman = hasilbagi[1]
                strPUteman = hasilbagi[2]
                bagiPUteman = strPUteman.split(">")
                PUteman = bagiPUteman[0]
                Nteman = bagiPUteman[1]
                deskeyteman = hasilbagi[3]

            else :
                #print 'recieved->  ',msg
                decDesMes = dekripsi(deskeyteman,msg)
                print 'recieved->  ',decDesMes.strip("~")

def setConn(con1,con2):
    dict={}
    state = con1.recv(9)
    con2.recv(9)
    if state =='WILL RECV':
        dict['send'] = con1 # server will send data to reciever
        dict['recv'] = con2
    else:
        dict['recv'] = con1 # server will recieve data from sender
        dict['send'] = con2
    return dict

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


(c1,a1) = soc.accept()
(c2,a2) = soc.accept()
dict = setConn(c1,c2)
thr = CThread(dict['recv'])
thr.start()
msend(dict['send'],CertificateA)
try:
    while 1:
        messageSend = raw_input()
        encryptDesMes = enkripsi(Mydeskey, messageSend)
        msend(dict['send'],encryptDesMes)
        print "print ulang ->>"+ encryptDesMes
        #print "print ulang ->>"+ CertificateB
        #print "print ulang ->>"+ deskeyteman
except:
    print 'closing'
thr.stopIt=True
msend(dict['send'],'bye!!!')# for stoping the thread
thr.conn.close()
soc.close()