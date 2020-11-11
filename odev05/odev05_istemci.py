#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 14:08:01 2020

@author: damla
"""

import socket


def main():
    global cikti
    ip="127.0.0.1"
    port = 8000
    
    s=socket.socket()

    saddr=(ip,port)
    
    s.connect(saddr)
    
    
    print("Selam, Naber, Hava, Haber ve Kapan komutlarindan birini giriniz.")
    print("\n Cikmak icin 'Kapan' komutunu giriniz.")
    soru=input("-")
    while soru != "Kapan":
        s.send(soru.encode())
        data=s.recv(1024)
        cevap=data.decode()
        print(cevap)
        soru=input("-")
    

    
    s.send(b"Kapan")
    
    
if __name__ == "__main__":
    main()