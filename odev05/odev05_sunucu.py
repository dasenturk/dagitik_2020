#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 13:56:15 2020

@author: damla
"""

import socket
import threading
import time

clientWords = ["Selam", "Naber", "Hava", "Haber", "Kapan"]
serverAnswers = ["Selam", "Iyiyim, sagol", "Yagmurlu", "Korona", "Gule gule"]
print_lock=threading.Lock()



class ConnectionThread(threading.Thread):
    def __init__(self, threadID, c, caddr):
        threading.Thread.__init__(self) 
        self.threadID = threadID
        self.c=c
        self.caddr=caddr
    def run(self):
        threaded(self.c) 
        
    
def cevapla(index):
    cevap=serverAnswers[index]
    print("Sunucunun cevabi:", cevap)
    return cevap

def sor(datastr):
    print("Istemcinin sordugu soru:", datastr)
    if datastr not in clientWords:
        sonuc="Anlamadim"
        print(sonuc)
    elif datastr == "Kapan":
        sonuc="Gule gule"
        print(sonuc)
    else:
        index=clientWords.index(datastr)
        sonuc = cevapla(index)
    return sonuc
    

def threaded(c):
    exitFlag=0
    while not exitFlag:
        data=c.recv(1024)
        datastr=data.decode().strip()
        soru=sor(datastr)
        if soru=="Gule gule":
            c.send(soru.encode())
            c.close()
            exitFlag=1
        else:
            c.send(soru.encode())
    c.close()
        
        
def main():  
    global exitFlag 
    
    #exitFlag=0
    
    s = socket.socket()

    ip="127.0.0.1"
    port = 8000
    
    saddr=(ip,port)
    s.bind(saddr)

    s.listen(5)
    threads=[]
    counter=0
    t=time.localtime()
    suan = time.strftime("%H:%M:%S", t)

    while True:
        c, addr = s.accept()
        print(addr, "adresine baglanildi. Saat su an", suan)
        #newConnectionThread=ConnectionThread(c,addr)
        newConnectionThread=ConnectionThread(counter,c,addr)
        threads.append(newConnectionThread)
        newConnectionThread.start()
        counter+=1
    
  
    s.close()
    
    
if __name__ == "__main__":
    main()