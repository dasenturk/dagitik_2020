#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 19:52:25 2020

@author: damla
"""

import socket
import threading
import queue
import time

noConnNeed = ["NIC", "QUI", "PIN"]
incomingCommands = ["NIC", "QUI", "GLS", "PIN", "GNL", "PRV"]
outgoingCommands = ["WEL", "REJ", "BYE", "PON", "LST", "OKG", "OKP", "NOP"]


class ReadThread(threading.Thread):
    def __init__(self, name, c, caddr, threadQueue, logQueue, fihrist):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.caddr = caddr
        self.threadQueue = threadQueue
        self.logQueue = logQueue
        self.nickname = ""
        self.fihrist = fihrist
    def incoming_parser(self, data):
        global log, response
        prm = data[4:]
        cmd = data[0:3]
        if len(cmd)<3:
            response = "ERR (1) \n" 
            log = "Server: " + response
            return response, log
        if len(cmd) > 3:
            response = "ERR (2) \n" 
            log = "Server: " + response
            return response, log
        if self.nickname == "" and cmd != "NIC":
            if cmd=="PIN":
                response = "PON\n"
                log = "Server: " + response
                #return response, log
            elif cmd=="QUI":
                response = "BYE\n"
                log = "Server: " + response
                #return response, log
            elif cmd not in noConnNeed:
                response = "LRR (1) \n"
                log = "Server: " + response
                #return response, log
        elif self.nickname == "" and cmd=="NIC":
            if prm == "":
                response = "ERR (3) \n" 
                log = "Server: " + response
            else:
                nickname=prm
                if nickname not in self.fihrist.keys():
                    self.nickname = nickname
                    response = "WEL " + nickname + "\n"
                    self.fihrist[self.nickname] = self.threadQueue
                    log = self.nickname + " has joined the chat.\n"
                else:
                    response = "REJ " + nickname + "\n"
                    log = "Server: " + response
            #return response, log
        elif self.nickname != "":
            if cmd == "QUI":
                response = "BYE " + self.nickname + "\n"
                self.fihrist.pop(self.nickname)
                log = self.nickname + " has left the chat.\n"
            elif cmd == "GLS":
                users = ""
                for key in self.fihrist.keys():
                    users += key + ":"
                users = users[:-1]
                response = "LST " + users + "\n"
                log = "Server: " + response
            elif cmd == "PIN":
                response = "PON\n"
                log = "Server: " + response
            elif cmd == "GNL":
                for key in self.fihrist.keys():
                    if key != self.nickname:
                        self.fihrist[key].put("GNL " + self.nickname + ": " + prm)
                response = "OKG\n"
                log = "Server: " + response
            elif cmd == "PRV":
                key, message = str.split(prm, ":", 1)
                if key not in self.fihrist.keys():
                    response = "NOP " + key + "\n"
                    log = "Server: " + response
                else:
                    self.fihrist[key].put("PRV " + self.nickname + ": " + message)
                    response = "OKP\n"
                    log = "Server: " + response
            else:
                response = "ERR (4) \n"
                log = "Server: " + response
        else:
            response = "ERR (5) \n"
            log = "Server: " + response
        return response, log
    def run(self):
        self.logQueue.put("Starting the " + self.name + "\n")
        exitFlag=0
        while not exitFlag:
            data = self.c.recv(1024)
            data = data.decode().strip()
            print ("Incoming data to the server: " + data)
            if self.nickname == "" :
                 self.logQueue.put("Client: " + data + "\n")
            else:
                self.logQueue.put(self.nickname + ": " + data + "\n")
            response, log = self.incoming_parser(data)
            self.logQueue.put(log)
            self.threadQueue.put(response)
            if data[0:3] == "QUI":
                #self.c.close()
                exitFlag=1
        self.logQueue.put("Ending connection with " + str(self.caddr) + "\n")
        self.logQueue.put("Exiting the " + self.name + "\n")
            
            
                


class WriteThread (threading.Thread):
    def __init__(self, name, c, caddr, threadQueue, logQueue, fihrist):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.caddr = caddr
        self.threadQueue = threadQueue
        self.logQueue = logQueue
        self.fihrist = fihrist
    def run(self):
        self.logQueue.put("Starting the " + self.name + "\n")
        exitFlag=0
        while not exitFlag:
            if not self.threadQueue.empty():
                queueMessage = self.threadQueue.get()
                print ("Outgoing data from the server: " + queueMessage)
                sent=queueMessage.encode()
                self.c.send(sent)
                if queueMessage[0:3] == "BYE":
                    self.c.close()
                    exitFlag=1
                else:
                    exitFlag=0
        #self.c.close()
        self.logQueue.put("Exiting the " + self.name + "\n")
        
        
        

class LoggerThread (threading.Thread):
    def __init__(self, name, logQueue, logFile):
        threading.Thread.__init__(self)
        self.name = name
        self.logQueue = logQueue
        self.fid=open(logFile, "a")
        #self.threadQueue = threadQueue
    def log(self, message):
        t = time.ctime()
        self.fid.write(t + " "  + message)
        self.fid.flush()
    def run(self):  
        self.log("Starting " + self.name + "\n") 
        while True:
            if self.logQueue.qsize() > 0:
                toBeLogged = self.logQueue.get()
                self.log(toBeLogged)
        self.log("Exiting " + self.name + "\n")
        self.fid.close()
            
        
def main():  
    global exitFlag
    
    s = socket.socket()
    host = "localhost"
    port = 12345
    s.bind((host, port))
    s.listen(5)
    
    fihrist=dict()
    lQueue=queue.Queue()
    counter=0
    
    logger = LoggerThread("LoggerThread", lQueue, "logFile.txt")
    logger.start()
   

    while True:
        sMessage = "Waiting for connection"
        print(sMessage)
        lQueue.put(sMessage + "\n")
        
        c, addr = s.accept()
        
        sMessage = "Got a connection from " + str(addr)
        print(sMessage)
        lQueue.put(sMessage  + "\n")
        
        counter +=1
        rThreadName = "ReadThread-" + str(counter)
        wThreadName = "WriteThread-" + str(counter)

        threadQueue = queue.Queue()
        
        rThread = ReadThread(rThreadName, c, addr, threadQueue, lQueue, fihrist)
        rThread.start()

        wThread = WriteThread(wThreadName, c, addr, threadQueue, lQueue, fihrist)  
        wThread.start() 
   
  
    
    
if __name__ == "__main__":
    main()
            
            
            
            
            
            
            
            
            
            
            
    