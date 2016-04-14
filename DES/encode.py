__author__ = 'Indra Gunawan'


message = [0,0,0,0, 0,0,0,1, 0,0,1,0, 0,0,1,1, 0,1,0,0, 0,1,0,1, 0,1,1,0, 0,1,1,1, 1,0,0,0, 1,0,0,1, 1,0,1,0, 1,0,1,1, 1,1,0,0, 1,1,0,1, 1,1,1,0, 1,1,1,1]
IP = [58,    50,   42,    34,    26,   18,    10,    2]
IP.extend( [60,    52,   44,    36,    28,   20,    12,    4] )
IP.extend([62,    54,   46,    38,    30,   22,    14,    6])
IP.extend([64,    56,   48,    40,    32,   24,    16,    8])
IP.extend([57,    49,   41,    33,    25,   17,     9,    1])
IP.extend([59,    51,   43,    35,    27,   19,    11,    3])
IP.extend([61,    53,   45,    37,    29,   21,    13,    5])
IP.extend([63,    55,   47,    39,    31,   23,    15,    7])


hasilIP = [None]*64

for x in range(0, len(IP)):
    a= IP[x]-1
    #print a
    tempmessage = message[a]
    #print tempKey
    hasilIP[x] = tempmessage
    #print key[a]

print hasilIP

leftM = hasilIP[:len(hasilIP)/2]
rightM = hasilIP[len(hasilIP)/2:]

print leftM
print rightM

