from DESwork import des

if __name__ == '__main__':
	IV = "kudaliar"
	msg = ["lari"]
	key = "12345678"

	b = len(IV)
	print "b=", b
	s = len(msg[0])
	print "s=", s

	def xor(message, key):
	   nilai_xor = [ int(message[x]) ^ int(key[x]) for x in range(len(message)) ]
	   message = "".join(str(x) for x in nilai_xor)
	   return message

	def enc(key, msg):
		return des(key).encrypt(msg)

	for i in range(0, 1):
	 	if i == 0 :
	 		#karena i=1 maka sama dengan iv
	 		y[i] = IV
	 	else :
	 		y[i] = y[i-1][b-s:]+c[i-1]

	 	#enkripsi DES
 		en = enc(key, y[i])
 		new_en = en[:s]

 		#xor dengan message
 		c[i] = xor(new_en, msg[i])
 		print c[i]

