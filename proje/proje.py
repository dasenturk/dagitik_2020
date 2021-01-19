#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:11:09 2021

@author: damla
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 23:04:21 2021

@author: damla
"""

import socket
import threading
import queue
import time

noConnNeed = ["NIC", "QUI", "PIN", "LOG"]
#incomingCommands = ["NIC", "QUI", "GLS", "PIN", "GNL", "PRV"]
#outgoingCommands = ["WEL", "REJ", "BYE", "PON", "LST", "OKG", "OKP", "NOP"]


class ReadThread(threading.Thread):
    def __init__(self, name, c, caddr, threadQueue, logQueue, fihrist, room, online):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.caddr = caddr
        self.threadQueue = threadQueue
        self.logQueue = logQueue
        self.nickname = ""
        self.sifre = ""
        self.fihrist = fihrist
        self.room = room
        self.online = online
        self.loggedIn = 0
        self.registered = 0
    def incoming_parser(self, data):
        global log, response
        cmd = data[0:3]
        parametre = data[4:]
        if parametre != "":
            if ":" in parametre:
                prm = parametre.split(":")
                prm1 = prm[0]
                prm2 = prm[1]
            else:
                prm1 = parametre
        if len(cmd)<3:
            response = "ERR (1) \n" 
            log = "Server: " + response
            return response, log
        if len(cmd) > 3:
            response = "ERR (2) \n" 
            log = "Server: " + response
            return response, log
        if self.registered == 0 and self.loggedIn == 0:
            if cmd=="PIN":
                response = "PON \n"
                log = "Server: " + response
                #return response, log
            elif cmd=="QUI":
                response = "BYE \n"
                log = "Server: " + response
                #return response, log
            elif cmd not in noConnNeed:
                response = "LRR (1) \n"
                log = "Server: " + response
                #return response, log
            elif cmd == "NIC" and self.nickname == "":
                if parametre == "":
                    response = "ERR (3) \n" 
                    log = "Server: " + response
                elif prm2 == "":
                    response = "ERR (4) \n"
                    log = "Server: " + response
                else:
                    nickname=prm1
                    sifre=prm2
                    if ((nickname,sifre) not in self.fihrist.keys()) and (nickname not in self.online.keys()):
                        self.nickname = nickname
                        self.sifre = sifre
                        self.fihrist[self.nickname, self.sifre] = self.threadQueue
                        response = "OKN " + nickname + "\n"
                        log = self.nickname + " has joined the chatroom.\n"
                        self.registered = 1
                    else:
                        response = "REJ " + nickname + "\n"
                        log = "Server: " + response
            else:
                response = "ERR (5) \n"
                log = "Server: " + response
        elif self.registered==1 and self.loggedIn==0:
            if cmd == "LOG":
                if parametre == "":
                    response = "ERR (6) \n" 
                    log = "Server: " + response
                elif prm2 == "":
                    response = "ERR (7) \n"
                    log = "Server: " + response    
                elif (prm1, prm2) not in self.fihrist.keys():
                    response = "LER \n"
                    log = "Server: " + response
                elif prm1 in self.online.keys():
                    response = "WER " + prm1 + "\n"
                    log = "Server: " + response
                else:
                    self.online[self.nickname] = self.threadQueue
                    response = "WEL " + prm1 + "\n"
                    log = "Server: " + response
                    self.loggedIn = 1
            elif cmd in noConnNeed:
                if cmd=="PIN":
                    response = "PON \n"
                    log = "Server: " + response
                elif cmd=="QUI":
                    response = "BYE \n"
                    log = "Server: " + response
            else:
                response = "ERR (8) \n"
                log = "Server: " + response
        elif self.registered==1 and self.loggedIn==1:
            if cmd == "NIC":
                if parametre == "":
                    response = "ERR (9) \n" 
                    log = "Server: " + response
                elif prm2 == "":
                    response = "ERR (10) \n"
                    log = "Server: " + response
                else:
                    nickname=prm1
                    sifre=prm2
                    if nickname not in self.online.keys():
                        response = "ERR (11) \n"
                        log = "Server: " +  response
                    elif nickname != self.nickname:
                        response = "ERR (12) \n"
                        log = "Server: " +  response
                    else:
                        self.sifre = sifre
                        response = "OKC " + nickname + "\n"
                        self.fihrist[self.nickname, self.sifre] = self.threadQueue
                        log = self.nickname + "'s password has been changed.\n"
            elif cmd == "QUI" and parametre == "":
                myRooms = [key
                           for key, list_of_values in self.room.items()
                           if self.nickname in list_of_values]
                response = "BYE " + self.nickname + "\n"
                self.fihrist.pop(self.nickname, self.sifre)
                self.online.pop(self.nickname)
                for item in myRooms:
                    self.room[item].pop(self.nickname)
                log = self.nickname + " has left the chat.\n"
                self.registered = 0
                self.loggedIn = 0
            elif cmd == "LOR" and parametre != "":
                if prm1 == "open":
                    rooms = ""
                    if len(self.room)<1:
                        rooms=""
                    else:
                        for key in self.room.keys():
                            rooms += key + ":"
                        rooms = rooms[:-1]
                    response = "LST " + rooms + "\n"
                    log = "Server: " + response
                elif prm1 == "me":
                    if len(self.room)<1:
                        myRooms=list()
                    else:
                        myRooms = [key
                                   for key, list_of_values in self.room.items()
                                   if self.nickname in list_of_values]
                    response = "LST " + ":".join(myRooms) + "\n"
                    log = "Server: " + response
                else:
                    response = "ERR (13) \n"
                    log = "Server: " +  response
            elif cmd == "NRM" and parametre != "":
                newRoom = prm1
                if newRoom not in self.room.keys():
                    self.room[newRoom] = dict()
                    self.room[newRoom][self.nickname] = "admin"
                    self.room[newRoom]["banned"] = list()
                    response = "OKR " + newRoom + "\n"
                    log = "New room " + newRoom + " has been opened.\n"
                else:
                    response = "NNR " + newRoom + "\n"
                    log = "Server: " + response
            elif cmd == "ERM" and parametre != "":
                if prm1 not in self.room.keys():
                    response = "NRR " + prm1 + "\n"
                    log = "Server: " + response
                else:
                    if (self.nickname not in self.room[prm1].keys()) and (self.nickname not in self.room[prm1]["banned"]) :
                        self.room[prm1][self.nickname] = "member"
                        for key in self.room[prm1].keys():
                            if key != self.nickname and key != "banned":
                                self.online[key].put("EDR " + self.nickname + "\n")
                        response = "WLR " + self.nickname + "\n"
                        log = "Server: " + response
                    elif self.nickname in self.room[prm1]["banned"]:
                        response = "RJR " + prm1 + "\n"
                        log = "Server: " + response
                    else: 
                        response = "AIR " + prm1 + "\n"
                        log = "Server: " + response
            elif cmd == "LRM" and parametre != "":
                if prm1 not in self.room.keys():
                    response = "NRR " + prm1 + "\n"
                    log = "Server: " + response
                else:
                    if self.nickname not in self.room[prm1].keys():
                        response = "NIR " + prm1 + "\n"
                        log = "Server: " + response
                    else:
                        self.room[prm1].pop(self.nickname)
                        for key in self.room[prm1].keys():
                            if key != self.nickname and key != "banned":
                                self.online[key].put("LDR " + self.nickname + "\n")
                        response = "BYR " + self.nickname + "\n"
                        log = "Server: " + response
            elif cmd == "KRM" and parametre !=  "":
                room = prm1
                person = prm2
                adminRooms = [key
                              for key, list_of_values in self.room[prm1].items()
                              if "admin" in list_of_values]
                if room not in self.room.keys():
                    response = "NRR " + room + "\n"
                    log = "Server: " + response
                elif self.nickname not in self.room[room].keys():
                    response = "NIR " + self.nickname + "\n"
                    log = "Server: " + response
                elif self.nickname not in adminRooms:
                    response = "AUT " + self.nickname + "\n"
                    log = "Server: " + response
                elif person not in self.online.keys():
                    response = "NOP " + person + "\n"
                    log = "Server: " + response
                elif person not in self.room[room].keys():
                    response = "NIR " + person + "\n"
                    log = "Server: " + response
                else:
                    self.room[room].pop(person)
                    self.online[person].put("NOR " + room + "\n")
                    for key in self.room[room].keys():
                        if key != self.nickname and key != "banned":
                            self.online[key].put("KDR " + person + "\n")
                    response = "KCK " + person + "\n"
                    log = "Server: " + response
            elif cmd == "ADM" and parametre !=  "":
                room = prm1
                person = prm2
                adminRooms = [key
                              for key, list_of_values in self.room[prm1].items()
                              if "admin" in list_of_values]
                if room not in self.room.keys():
                    response = "NRR " + room + "\n"
                    log = "Server: " + response
                elif self.nickname not in self.room[room].keys():
                    response = "NIR " + self.nickname + "\n"
                    log = "Server: " + response
                elif self.nickname not in adminRooms:
                    response = "AUT " + self.nickname + "\n"
                    log = "Server: " + response
                elif person not in self.online.keys():
                    response = "NOP " + person + "\n"
                    log = "Server: " + response
                elif person not in self.room[room].keys():
                    response = "NIR " + person + "\n"
                    log = "Server: " + response
                else:
                    self.room[room][person] = "admin"
                    self.online[person].put("CNA " + room + "\n")
                    for key in self.room[room].keys():
                        if key != self.nickname and key != "banned":
                            self.online[key].put("CNG " + person + "\n")
                    response = "OKA " + person + "\n"
                    log = "Server: " + response
            elif cmd == "BAN" and parametre !=  "":
                room = prm1
                person = prm2
                adminRooms = [key
                              for key, list_of_values in self.room[prm1].items()
                              if "admin" in list_of_values]
                if room not in self.room.keys():
                    response = "NRR " + room + "\n"
                    log = "Server: " + response
                elif self.nickname not in self.room[room].keys():
                    response = "NIR " + self.nickname + "\n"
                    log = "Server: " + response
                elif self.nickname not in adminRooms:
                    response = "AUT " + self.nickname + "\n"
                    log = "Server: " + response
                elif person not in self.online.keys():
                    response = "NOP " + person + "\n"
                    log = "Server: " + response
                elif person not in self.room[room].keys():
                    response = "NIR " + person + "\n"
                    log = "Server: " + response
                else:
                    self.room[room].pop(person)
                    self.room[room]["banned"].append(person)
                    self.online[person].put("NOB " + room + "\n")
                    for key in self.room[room].keys():
                        if key != self.nickname and key != "banned":
                            self.online[key].put("BON " + person + "\n")
                    response = "OKB " + person + "\n"
                    log = "Server: " + response
            elif cmd == "DRM" and parametre !=  "":
                adminRooms = [key
                              for key, list_of_values in self.room[prm1].items()
                              if "admin" in list_of_values]
                if prm1 not in self.room.keys():
                    response = "NRR " + room + "\n"
                    log = "Server: " + response
                elif self.nickname not in self.room[prm1].keys():
                    response = "NIR " + person + "\n"
                    log = "Server: " + response
                elif self.nickname not in adminRooms:
                    response = "AUT " + self.nickname + "\n"
                    log = "Server: " + response
                else:
                    for key in self.room[prm1].keys():
                        if key != self.nickname and key != "banned":
                            self.online[key].put("CLO " + prm1 + "\n")
                    self.room.pop(prm1)
                    response = "OKD " + prm1 + "\n"
                    log = prm1 + " has been closed.\n"
            elif cmd == "PRV" and parametre != "":
                person = prm1
                message = prm2
                if person not in self.online.keys():
                    response = "NOP " + person + "\n"
                    log = "Server: " + response
                else:
                    self.online[person].put("PRV " + self.nickname + ": " + message + "\n")
                    response = "OKP \n"
                    log = "Server: " + response
            elif cmd == "GNL" and parametre != "":
                room = prm1
                message = prm2
                if room not in self.room.keys():
                    response = "NRR " + room + "\n"
                    log = "Server: " + response
                elif self.nickname not in self.room[room].keys():
                    response = "NIR " + room + "\n"
                    log = "Server: " + response
                else:
                    for key in self.room[room].keys():
                        if key != self.nickname and key != "banned":
                            self.online[key].put("GNL " + self.nickname + ": " + message + "\n")
                    response = "OKG \n"
                    log = "Server: " + response  
            elif cmd == "GLS" and parametre != "":
                users = ""
                for rid, rinfo in self.room.items():
                    if rid == prm1:
                        for key in rinfo:
                            if key != "banned":
                                users += str(key) + "-" + str(rinfo[key]) + ":"
                users = users[:-1]
                response = "LST " + users + "\n"
                log = "Server: " + response
            elif cmd == "PIN" and parametre == "":
                response = "PON \n"
                log = "Server: " + response
            else:
                response = "ERR (14) \n"
                log = "Server: " + response
        else:
            response = "ERR (15) \n"
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
                exitFlag=1
        self.logQueue.put("Ending connection with " + str(self.caddr) + "\n")
        self.logQueue.put("Exiting the " + self.name + "\n")
            
            
    

class WriteThread (threading.Thread):
    def __init__(self, name, c, caddr, threadQueue, logQueue, fihrist, room, online):
        threading.Thread.__init__(self)
        self.name = name
        self.c = c
        self.caddr = caddr
        self.threadQueue = threadQueue
        self.logQueue = logQueue
        self.fihrist = fihrist
        self.room = room
        self.online = online
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
        self.logQueue.put("Exiting the " + self.name + "\n")
        
        
        

class LoggerThread (threading.Thread):
    def __init__(self, name, logQueue, projeLogger):
        threading.Thread.__init__(self)
        self.name = name
        self.logQueue = logQueue
        self.fid=open(projeLogger, "a")
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
    room=dict()
    online=dict()
    lQueue=queue.Queue()
    counter=0
    
    logger = LoggerThread("LoggerThread", lQueue, "projeLogger.txt")
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
        
        rThread = ReadThread(rThreadName, c, addr, threadQueue, lQueue, fihrist, room, online)
        rThread.start()

        wThread = WriteThread(wThreadName, c, addr, threadQueue, lQueue, fihrist, room, online)  
        wThread.start() 
   
  
    
    
if __name__ == "__main__":
    main()
            
