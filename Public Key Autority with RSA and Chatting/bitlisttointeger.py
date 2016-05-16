__author__ = 'Indra Gunawan'

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

hel = "hello"
hel2 = str_ke_bitlist(hel)
hel3 = intcaststr(hel2)

lol = [1,0,0,0]
lol2 = [1,0,0]
wow = intcaststr(lol)
yolo = bitfield(wow)

wow2 = intcaststr(lol2)
lol3 = wow + wow2

print lol3
print yolo
print hel3