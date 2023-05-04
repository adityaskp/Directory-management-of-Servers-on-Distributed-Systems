#NAME - ADITYA SHIVAJI PATIL
#STUDENT ID-1001995431
#Reference for pickle library - https://realpython.com/python-pickle-module/
import socket
import os #for getting details of directories
import glob
import time
import pickle #serializing and deserializing with the Python pickle module.
HOST = '10.199.144.217'
PORT = 3000
i=0

#connect to server_a
while True:
    #time.sleep(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    data = s.recv(1024)
    print(data.decode("utf-8"))
    info = s.recv(2048)
    all = pickle.loads(info)
    i=0
    for x in all:
        print(all[i])
        i=i+1
    inputuser=input("Please enter the input:  ")#user input
    s.send(inputuser.encode())#sending to servera
    #print("File locked is", inputuser)
    command=inputuser.split(' ',1)
    if command[0] == "lock":
        field=all[int(command[1])-1]
        file=field.split(' ',2)
        print("File locked is - ",file[1])
    if command[0] == "unlock":
        field=all[int(command[1])-1]
        file=field.split(' ',2)
        print("File unlocked is - ",file[1])
