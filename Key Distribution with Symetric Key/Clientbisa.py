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

	if "REQ" in cmd:
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
