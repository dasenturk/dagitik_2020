#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 12:32:17 2020

@author: damla
"""

import threading
import sys
import socket
import random

istemciKomut = ["STA", "TRY", "TIC", "QUI"]


class ConnectionThread(threading.Thread):
    def __init__(self, threadID, c, caddr, name):
        threading.Thread.__init__(self) 
        self.threadID = threadID
        self.c=c
        self.caddr=caddr
        self.name = name
    def run(self):
        threaded(self.c) 

def receive(datastr):
    if datastr not in istemciKomut:
        cevap="ERR"
        #break
    elif datastr != "STA":
        if datastr == "TIC":
            cevap="TOC"
        else:
            cevap="GRR"
            #break
    else:
        cevap="RDY"
    return cevap

def oyun(komutstr, n):
    if len(komutstr) != 2:
        if len(komutstr)==1:
            if komutstr=="TIC":
                cvp = "TIC"
            elif komutstr=="QUI":
                cvp = "BYE"
            else:
                cvp = "ERR"
        else:
            cvp = "ERR"
    else:
        if komutstr[0] == "TRY":
            sayi = int(komutstr[1])
            if type(sayi) != int:
                cvp = "ERR"
            elif sayi>n:
                cvp = "GTH"
            elif sayi<n:
                cvp = "LTH"
            elif sayi == n:
                cvp = "WIN"
            else:
                cvp = "ERR"
        else:
            cvp = "ERR"
    return cvp
        

def threaded(c):
    exitFlag=0
    while not exitFlag:
        data=c.recv(1024)
        datastr=data.decode().strip()
        cvp=receive(datastr)
        c.send(cvp.encode())
        #her seferinde yeni sayi atiyo bu kismi duzeltmeyi yetistiremedim
        n=random.randint(0,100)
        while cvp == "RDY":
            komut=c.recv(1024)
            komutstr=komut.decode().strip().split()
            ans = oyun(komutstr,n)
            c.send(ans.encode())
            if ans == "QUI" or ans == "WIN":
                c.close()
                exitFlag=1
    c.close()

def main():  
    global exitFlag
    
    if not len(sys.argv) == 3:
        print("Insufficient parameters")
        return
    
    port = int(sys.argv[2])
    ipaddr = sys.argv[1]
    saddr=(ipaddr, port)
    
    s = socket.socket()
    s.bind(saddr)
    s.listen(5)
    threads=[]
    counter=0
   

    while True:
        c, addr = s.accept()
        c.send(b"Sayi bulmaca oyununa hosgeldiniz!")
        newConnectionThread=ConnectionThread(counter,c,addr, "Thread-"+str(counter))
        threads.append(newConnectionThread)
        newConnectionThread.start()
        counter+=1
   
  
    s.close()
    
    
if __name__ == "__main__":
    main()
