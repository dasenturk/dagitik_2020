#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 13:46:02 2020

@author: damla
"""

from multiprocessing import Process, Queue, Lock, current_process
import sys

alphabet="abcdefghijklmnopqrstuvwxyz"
queueLock=Lock()


def encrypt(text):
    encrypted=""
    for i in text:
        if i not in alphabet:
            encrypted += i
        else:
            encrypted += alphabet[(alphabet.index(i) + s)%26]
    return encrypted


def caesarChipper(workQueue, doneQueue):
    while not workQueue.empty():
        queueLock.acquire()
        data = workQueue.get()
        data=data.lower()
        data2 = encrypt(data)
        doneQueue.put(data2)
        #outputcaesar.write(data2)
        queueLock.release()
    while not doneQueue.empty():
        text=doneQueue.get()
        outputcaesar.write(text)
        #outputcaesar.close()
        
               

def main():
    global s,n,l
    global inputcaesar,outputcaesar
    workQueue=Queue()
    doneQueue=Queue()
    
    if len(sys.argv)!=4:
        print("Invalid number of parameters. Please try again")
        sys.exit()
    else:
        s=int(sys.argv[1])
        n=int(sys.argv[2])
        l=int(sys.argv[3])
        
    try:
        inputcaesar = open("input.txt", "r")
        outputcaesar = open("crypted_fork_%d_%d_%d.txt" % (s, n, l), "w")
    except:
        print ("Opening failed")
        sys.exit()
        
    processList=[]
    for i in range(0,n):
        p = Process(target=caesarChipper, args=(workQueue, doneQueue))
        p.start()
        print(p)
        processList.append(p)
        
    queueLock.acquire()
    while True:
        string = inputcaesar.read(l)
        if string != "":
            workQueue.put(string)
        else:
            break
    queueLock.release()
        
    
    #doneQueue.put("STOP")
    
    for p in processList:
        p.join()
        print(p)
        
    inputcaesar.close()
    outputcaesar.close()
    

if __name__ == "__main__":
    main()