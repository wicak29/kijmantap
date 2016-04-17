__author__ = 'Indra Gunawan'
import sys
import os,socket,threading,time

server_address = ('192.168.0.23', 8000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)

client.settimeout(3)
data = ""
data = client.recv(1024)
print data

while(1):
	cmd = raw_input(">>")
	print cmd
	if "LIST" in cmd:
		cmd = client.send(cmd+"\r\n")
		#data = client.recv(1024)
		while True:
			data = client.recv(1024)
			print data
			if "Directory send OK." in data:
				break
	elif "STOR" in cmd:
		namafile = cmd.split("STOR ",1)[1]
		size=os.stat(namafile).st_size
		cmd = client.send(cmd+"\r\n")
		print client.recv(4096)
		f = open(namafile, "rb")
		data = f.read()
		f.close()
		client.send(str(size)+'\r\n\r\n'+data)
		print client.recv(4096)
	elif "DELE" in cmd:
		cmd = client.send(cmd+"\r\n")
		data = client.recv(1024)
		print data
	elif "CWD" in cmd:
		cmd = client.send(cmd+"\r\n")
		data = client.recv(1024)
		print data
	elif "PWD" in cmd:
		cmd = client.send(cmd+"\r\n")
		data = client.recv(1024)
		print data
	elif "HELP" in cmd:
		cmd = client.send(cmd+"\r\n")
		data = client.recv(1024)
		print data
	elif "USER" in cmd:
		cmd = client.send(cmd+"\r\n")
		data = client.recv(1024)
		print data
	elif "PASS" in cmd:
		cmd = client.send(cmd+"\r\n")
		data = client.recv(1024)
		print data
	elif "QUIT" in cmd:
		cmd = client.send(cmd+"\r\n")
		data = client.recv(1024)
		client.close()
		print data
		exit()
	elif "RNTO" in cmd:
		cmd = client.send(cmd+"\r\n")
		data = client.recv(1024)
		print data
	elif "RNFR" in cmd:
		cmd = client.send(cmd+"\r\n")
		data = client.recv(1024)
		print data
	elif "MKD" in cmd:
		cmd = client.send(cmd+"\r\n")
		data = client.recv(1024)
		print data
	elif "RMD" in cmd:
		cmd = client.send(cmd+"\r\n")
		data = client.recv(1024)
		print data

	elif "RETR" in cmd:
		filename = cmd.split("RETR ",1)[1]
		cmd = client.send(cmd+"\r\n")
		comm = client.recv(1024)
		print comm
		data = client.recv(1024)
		print data
		#dat = client.recv(1024)
		if data[:6] == 'EXISTS':
			#print comm
			filesize = long(data[6:])
			#print filesize

			#message = raw_input("File exists, " + str(filesize) +"Bytes, download? (Y/N)? -> ")
			f = open(filename, 'wb')
			data = client.recv(1024)
			#print data
			totalRecv = len(data)
			#print totalRecv

			f.write(data)

			while totalRecv < filesize:
				data = client.recv(1024)
				totalRecv += len(data)
				f.write(data)
				#print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
			print "Download Complete!"
			f.close()
			com = client.recv(1024)
			print com


			#print comm

		else:
			print "File Does Not Exist!"