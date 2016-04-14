__author__ = 'Indra Gunawan'



def xor(message, key):
   nilai_xor = [ int(message[x]) ^ int(key[x]) for x in range(len(message)) ]
   message = "".join(str(x) for x in nilai_xor)
   return message

print xor("101","100")




