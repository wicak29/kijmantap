__author__ = 'Indra Gunawan'
from DESwork import des

if __name__ == '__main__':
    '''
        Definisi Pesan dan Kunci harus 64 bit / 8 character
    '''
    #key = '12345678'
    #mess = '87654321'
    IV = 'kudalari'
    key = '12345678'
    mess = 'liar'

    #x = des(key).encrypt(mess)
    #print x

    #y = des(key).decrypt(x)
    #print y

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

    #x0 = str_ke_bitlist(IV)
    #print x0

    hasil0 = des(key).encrypt(IV)
    print "encrypt : ", hasil0
    print "decrypt : ", des(key).decrypt(hasil0)
    dibagi0 = str_ke_bitlist(hasil0)
    print dibagi0

    Sleft0 = dibagi0[:len(dibagi0)/2]
    Sright0 = dibagi0[len(dibagi0)/2:]

    print Sleft0
    #print Sright0

    m0 = str_ke_bitlist(mess)
    print m0
    c1 = map(lambda x, y: x^y, m0,Sleft0 )
    print c1

    x1 = Sright0 + c1

    print "x1 :", x1


    print bitlist_ke_str(c1)












