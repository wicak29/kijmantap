__author__ = 'Indra Gunawan'

import os
import socket
import threading
import re
import time
import subprocess
import uuid
import random
import string

hapus = True
local_ip = ('192.168.0.23')
local_port = 8000
currdir=os.path.abspath('.')

class FTPserverThread(threading.Thread):
    def __init__(self,(conn,addr)):
        self.conn=conn
        self.addr=addr
        self.basewd=currdir
        self.cwd=self.basewd
        self.rest=False
        self.namaKlien=""
        self.pasv_mode=True
        self.user_pass=[["123","123"],["321","321"]]
        self.user_session=[["","",""]]
        threading.Thread.__init__(self)

    def run(self):
        self.conn.send('220 Welcome!\r\n')
        while True:
            cmd=self.conn.recv(256)
            if not cmd: break
            else:
                print 'Recieved:',cmd
                try:
                    func=getattr(self,cmd[:4].strip().upper())
                    func(cmd)
                except Exception,e:
                    print 'ERROR:',e
                    #traceback.print_exc()
                    self.conn.send('500 Syntax error, command unrecognized.\r\n')

    def REQ(self, cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                print "request diterima"
                #self.conn.send("request diterima")
                listkey = [random.choice(string.ascii_letters + string.digits) for n in xrange(8)]
                print listkey
                randomsessionkey = "".join(listkey)
                self.conn.send(randomsessionkey)
                print "request dikirim"

                #pesan = "USER PASS QUIT PWD CWD LIST MKD RMD DELE RNFR RNTO RETR STOR HELP\r\n"
                #self.conn.send(pesan)
                break
            elif i==len(self.user_session)-1:
                self.conn.send('530 Please Login with USER and PASS.\r\n')
    def USER(self,cmd):
        namaKlien=cmd.split(" ")
        for i in range (0,len(self.user_pass)):
            print namaKlien[1][:-2]+"--",self.user_pass[i][0]
            if namaKlien[1][:-2] == self.user_pass[i][0]:
                self.conn.send('331 Please specify the password\r\n')
                self.user_session.append([self.conn.getpeername(),namaKlien[1][:-2],"not ok"])
                break
            elif i==len(self.user_session):
                self.conn.send('530 Please Login with USER and PASS.\r\n')
    def PASS(self,cmd):
        passKlien=cmd.split(" ")[1].strip("\r\n")
        namaKlien=""
        index = 0
        ipPort=self.conn.getpeername()
        print ipPort
        for i in range (0,len(self.user_session)):
            if ipPort==self.user_session[i][0]:
                namaKlien=self.user_session[i][1]
                index=i
                break
        passServer=""
        for i in range (0,len(self.user_pass)):
            if namaKlien == self.user_pass[i][0]:
                passServer=self.user_pass[i][1]
                break
        if passServer==passKlien:
            self.user_session[index][2]="OK"
            self.conn.send('230 User logged in, proceed.\r\n')
        else:
            del self.user_session[index]
            self.conn.send('530 Login incorrect.\r\n530 Please Login with USER and PASS.\r\n')
    def QUIT(self,cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0]:
                del self.user_session[i]
        self.conn.send("221 Goodbye.\r\n")



class FTPserver(threading.Thread):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((local_ip,local_port))
        threading.Thread.__init__(self)

    def run(self):
        self.sock.listen(5)
        while True:
            th=FTPserverThread(self.sock.accept())
            th.daemon=True
            th.start()

    def stop(self):
        self.sock.close()

if __name__=='__main__':
    ftp=FTPserver()
    ftp.daemon=True
    ftp.start()
    print 'On', local_ip, ':', local_port
    raw_input('Enter to end...\n')
    ftp.stop()