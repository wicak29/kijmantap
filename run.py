__author__ = 'Indra Gunawan'
from DESwork import des

if __name__ == '__main__':
    '''
        Definisi Pesan dan Kunci harus 64 bit / 8 character
    '''
    #key = '12345678'
    #mess = '87654321'
    key = '12345678'
    mess = 'kudaliar'


    x = des(key).encrypt(mess)
    print x

    y = des(key).decrypt(x)
    print y