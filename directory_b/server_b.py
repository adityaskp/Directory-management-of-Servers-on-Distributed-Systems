#NAME - ADITYA SHIVAJI PATIL
#STUDENT ID-1001995431
# Reference - https://www.tutorialspoint.com/python/os_listdir.htm
# Reference - https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
# Reference - http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
import socket
import os #for getting details of directories
import glob
import time
import pickle # serializing and deserializing with the Python pickle module.



file_s = []#to store the files name in string format
local_t= []#to store the modification_time of file in string format
i=0
HOST = '10.199.144.217' # is the standard IPv4 address for the loopback interface
PORT = 3001 #port numer
#socket.socket - creates a socket obect  AF_INET- socket family(ipv4) , SOCK_STREAM- type of socket(TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)
while True:
    conn, addr = s.accept()
    print('connected by', addr)
    conn.send(bytes("Welcome to the server2!","utf-8"))
    list_of_files=os.listdir()#os command to get the list of files
    list_of_files= sorted( list_of_files, key = os.path.getmtime)#sorting files list by key-modification_time
    for files in list_of_files:
        path=str(files)#storing as string for sending using pickle
        file_size = os.path.getsize(path)
        file_s.append(str(file_size))
        modification_time = os.path.getmtime(path)
        local_time = time.ctime(modification_time)
        local_t.append(str(local_time))
        print(files,file_size,"bytes",local_time)
        i=i+1
    cour=0
    #packing file name,file size,file modification time in a single list
    all=[]
    for q in range(len(list_of_files)):
        qtemp = list_of_files[cour],file_s[cour],local_t[cour]
        all.append(qtemp)
        cour=cour+1
    info=pickle.dumps(all)
    conn.send(info)
    path='C:/Users/adity/OneDrive/Desktop/submit/directory_b'
    before = os.listdir(path)
    added=[]
    removed=[]
    temp=0
    while True:
        after = os.listdir(path) # new updated list of directories
        check=0
        if len(after) > len(before): #if updated list bigger
            for fa in after:
                for fb in before:
                    if fa == fb:#Check if name of files same
                        check=10
                if check == 0:
                    added.append(fa) # add the file name in added list
                check=0
        if len(before)>len(after):  # if updated list smaller
            for fb in before:
                for fa in after:
                    if fa == fb: #Check if name of files same
                        check=10
                if check == 0:
                    removed.append(fb) # add the file name in the removed list
                check=0

        if len(added)!=0: #if list is empty
            for i in added:
                print("Added: ",i)
        if len(removed)!=0: #if list is empty
            for i in removed:
                print("Removed: ",i)

        before=after
        added.clear()
        removed.clear()
