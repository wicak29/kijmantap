__author__ = 'Indra Gunawan'
import socket
from thread import *
from time import sleep
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.23', 8888))
#u = raw_input('Username: ')
#print 'To send: recipient>message'
'''
def send(s):
    while 1:
        s.send(u + '>' + raw_input())
        print s.recv(1024)
'''

'''
def receive(s):
    while 1:
        s.send(u + '>show>')
        r = s.recv(1024)
        if r != 'No messages':
            print r
        sleep(0.05)
'''
'''
def terimarequest(s):
    while 1:
        cmd = raw_input(">>")
        #print cmd
        if "request" in cmd:
            cmd = s.send(cmd+"\r\n")
            data = s.recv(1024)
            print data

#start_new_thread(send ,(s,))
#start_new_thread(receive ,(s,))
start_new_thread(terimarequest ,(s,))
'''
idA = " alice"
idB = " bob"
Nance = " 73"
while 1:
    cmd = raw_input(">>")
    #print cmd
    if "request" in cmd:
        cmd = s.send(cmd+idA+idB+Nance+"\r\n")
        data = s.recv(1024)
        print data


