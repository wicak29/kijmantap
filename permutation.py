
key = [0,0,0,1,0,0,1,1, 0,0,1,1,0,1,0,0, 0,1,0,1,0,1,1,1, 0,1,1,1,1,0,0,1, 1,0,0,1,1,0,1,1, 1,0,1,1,1,1,0,0, 1,1,0,1,1,1,1,1, 1,1,1,1,0,0,0,1]
PC1 = [57,  49,    41,   33,    25,    17,    9]
PC1.extend( [1,   58,   50,   42,   34,   26,   18] )
PC1.extend([10,    2,    59,   51,    43,    35,   27])
PC1.extend([19,   11,     3,   60,    52,    44,   36])
PC1.extend([63,   55,    47,   39,    31,    23,   15])
PC1.extend([7,   62,    54,   46,    38,    30,   22])
PC1.extend([14,    6,    61,   53,    45,    37,   29])
PC1.extend([21,   13,     5,   28,    20,    12,    4])

#Kp adalah Key yang akan dipermutasi, inisialisasi dengan angka selain 0 dan 1
Kp = [8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8, 8,8,8,8,8,8,8,8]

for x in range(0, len(PC1)):
    a = PC1[x]-1
    tempKey = key[a]
    Kp[x] = tempKey

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

#print Kp
C0 = halfK(0, (len(Kp)/2), Kp)
print C0
D0 = halfK((len(Kp)/2), len(Kp), Kp)
print D0

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




#print C1


