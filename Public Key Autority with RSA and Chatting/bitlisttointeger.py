__author__ = 'Indra Gunawan'

def intcaststr(bitlist):
    return int("".join(str(i) for i in bitlist), 2)


def bitfield(n):
    return [1 if digit=='1' else 0 for digit in bin(n)[2:]]

lol = [1,0,0,0]
lol2 = [1,0,0]
wow = intcaststr(lol)
yolo = bitfield(wow)

wow2 = intcaststr(lol2)
lol3 = wow + wow2

print lol3
print yolo