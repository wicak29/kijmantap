__author__ = 'Indra Gunawan'

import os
import socket
import threading
import re
import time
import subprocess
import uuid
import md5, base64, random

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
    def generate_key(self, uid):

        my_id = uuid.uuid4()
        m.update(os.urandom(random.randint(15,25)))
        m.update(uid)
        return base64.standard_b64encode(m.digest())

    def HELP(self, cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                pesan = "USER PASS QUIT PWD CWD LIST MKD RMD DELE RNFR RNTO RETR STOR HELP\r\n"
                self.conn.send(pesan)
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
        self.conn.send("221 Goodbye.\r\n");
    def PWD(self,cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                cwd=os.path.relpath(self.cwd,self.basewd)
                if cwd=='.':
                    cwd='/'
                else:
                    cwd='/'+cwd
                self.conn.send('200 Command okay \"%s\"\r\n' % cwd)
                break
            elif i==len(self.user_session)-1:
                self.conn.send('530 Please Login with USER and PASS.\r\n')
    def CWD(self,cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                chwd=cmd[4:-2]
                if chwd=='/':
                    self.cwd=self.basewd
                elif chwd[0]=='/':
                    self.cwd=os.path.join(self.basewd,chwd[1:])
                else:
                    self.cwd=os.path.join(self.cwd,chwd)
                self.conn.send('200 Command okay.\r\n')
            elif i==len(self.user_session)-1:
                self.conn.send('530 Please Login with USER and PASS.\r\n')
    def start_datasock(self):
        if self.pasv_mode:
            self.datasock, addr = self.servsock.accept()
            print 'connect:', addr
        else:
            self.datasock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.datasock.connect((self.dataAddr,self.dataPort))

    def stop_datasock(self):
        self.datasock.close()
        if self.pasv_mode:
            self.servsock.close()

    def LIST(self,cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                self.conn.send('150 Here comes the directory listing.\r')
                print 'list:', self.cwd
                datas = ""
                for filename in os.listdir(self.cwd):
                        data = filename
                        datas=datas+'\n'+data
                self.conn.send(datas+'\n')
                self.conn.send('226 Directory send OK.\r\n')
            elif i==len(self.user_session)-1:
                self.conn.send('530 Please Login with USER and PASS.\r\n')
    def MKD(self,cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                dn=os.path.join(self.cwd,cmd[4:-2])
                os.mkdir(dn)
                self.conn.send('257 Directory created.\r\n')
            elif i==len(self.user_session)-1:
                self.conn.send('530 Please Login with USER and PASS.\r\n')
    def RMD(self,cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                dn=os.path.join(self.cwd,cmd[4:-2])
                if hapus:
                    os.rmdir(dn)
                    self.conn.send('250 Directory deleted.\r\n')
                else:
                    self.conn.send('450 Not allowed.\r\n')
            elif i==len(self.user_session)-1:
                self.conn.send('530 Please Login with USER and PASS.\r\n')
    def DELE(self,cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                fn=os.path.join(self.cwd,cmd[5:-2])
                if hapus:
                    os.remove(fn)
                    self.conn.send('250 File deleted.\r\n')
                else:
                    self.conn.send('450 Not allowed.\r\n')
            elif i==len(self.user_session)-1:
                self.conn.send('530 Please Login with USER and PASS.\r\n')
    def RNFR(self,cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                self.rnfn=os.path.join(self.cwd,cmd[5:-2])
                self.conn.send('350 Ready.\r\n')
            elif i==len(self.user_session)-1:
                self.conn.send('530 Please Login with USER and PASS.\r\n')
    def RNTO(self,cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                fn=os.path.join(self.cwd,cmd[5:-2])
                os.rename(self.rnfn,fn)
                self.conn.send('250 File renamed.\r\n')
            elif i==len(self.user_session)-1:
                self.conn.send('530 Please Login with USER and PASS.\r\n')
    def RETR(self,cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                fn=os.path.join(self.cwd,cmd[5:-2])
                self.conn.send('150 Opening data connection.\r\n')
                if os.path.isfile(fn):

                        self.conn.send("EXISTS " + str(os.path.getsize(fn)))
                        print 'Downloading:',fn
                        i=0
                        with open(fn, 'rb') as f:
                                bytesToSend = f.read(1024)
                                self.conn.send(bytesToSend)
                                while bytesToSend != "":
                                        bytesToSend = f.read(1024)
                                        self.conn.send(bytesToSend)
                                        print "prosessing"
                                self.conn.send('226 Transfer complete.\r\n')
                else:
                        self.conn.send("ERR ")
            elif i==len(self.user_session)-1:
                self.conn.send('530 Please Login with USER and PASS.\r\n')
    def STOR(self,cmd):
        for i in range (0, len(self.user_session)):
            if self.conn.getpeername()==self.user_session[i][0] and self.user_session[i][2]=="OK":
                fn=os.path.join(self.cwd,cmd[5:-2])
                print 'Uplaoding:',fn
                fo=open(fn,'wb')
                self.conn.send('150 Opening data connection.\r\n')
                i=0
                buf=self.conn.recv(4096)
                size=int(buf.split('\r\n\r\n')[0])
                data='\r\n\r\n'.join(buf.split('\r\n\r\n')[1:])
                size=size-len(data)
                while i<size:
                    data+=self.conn.recv(4096)
                    i=i+4096
                fo.write(data)
                fo.close()
                self.conn.send('226 Transfer complete.\r\n')
            elif i==len(self.user_session)-1:
                self.conn.send('530 Please Login with USER and PASS.\r\n')

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