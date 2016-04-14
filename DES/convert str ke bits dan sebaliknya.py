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

key = "0123456789ABCDEF"
# hexKey = ":".join("{:02x}".format(ord(c)) for c in key)
# print "hexKey : ", hexKey
hexKey = ''.join(format(ord(x), 'b') for x in key)
print "hexKey : ", hexKey

print "key : ", str_ke_bitlist(key)
print len(str_ke_bitlist(key))

hasil1 = str_ke_bitlist(key)
print hasil1
print len(hasil1)

hasil2 = bitlist_ke_str(hasil1)
print hasil2

# #String to hexa decimal
# my_hexdata = "133457799BBCDFF1"
# scale = 16 ## equals to hexadecimal
# num_of_bits = 4
# result = bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
# print result
# print len(result)