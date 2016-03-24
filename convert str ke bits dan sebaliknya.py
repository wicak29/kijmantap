__author__ = 'Indra Gunawan'

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


hasil1 = str_ke_bitlist("Informatika")
print hasil1

hasil2 = bitlist_ke_str(hasil1)
print hasil2
