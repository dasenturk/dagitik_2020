#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 00:10:45 2020

@author: damla
"""

import threading
import queue
import sys

exitFlag = 0
alphabet="abcdefghijklmnopqrstuvwxyz"
queueLock = threading.Lock()
#key=0
workQueue = queue.Queue()
    

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self) 
        self.threadID = threadID
        self.name = name 
        self.q = q
    def run(self):
        print("Starting " + self.name)
        process_data(self.name, self.q) 
        print("Exiting " + self.name)

def process_data(name,q):
    while not exitFlag:
        queueLock.acquire() 
        if not workQueue.empty():
            data = q.get()
            data=data.lower()
            data2 = encrypt(data)
            outputcaesar.write(data2)
            queueLock.release()
        else:
            queueLock.release()
        #time.sleep(1)
        

def encrypt(text):
    encrypted=""
    for i in text:
        if i not in alphabet:
            encrypted += i
        else:
            encrypted += alphabet[(alphabet.index(i) + s)%26]
    return encrypted

      

def main():
    global s,n,l
    global workQueue, exitFlag
    global inputcaesar,outputcaesar
    
    if len(sys.argv)!=4:
        print("Invalid number of parameters. Please try again")
        sys.exit()
    else:
        s=int(sys.argv[1])
        n=int(sys.argv[2])
        l=int(sys.argv[3])
        
    try:
        inputcaesar = open("input.txt", "r")
        outputcaesar = open("crypted_thread_%d_%d_%d.txt" % (s, n, l), "w")
    except:
        print ("Opening failed")
        sys.exit()
        
    threadList=[]
    for i in range(1,n+1):
        thread=myThread(i, "Thread-" + str(i), workQueue)
        thread.start()
        threadList.append(thread)
        
    while True:
        string = inputcaesar.read(l)
        if string != "":
            workQueue.put(string)
        else:
            break
    while not workQueue.empty():
        pass
    exitFlag = 1
    
    for t in threadList:
        t.join()
        
    inputcaesar.close()
    outputcaesar.close()
    

if __name__ == "__main__":
    main()