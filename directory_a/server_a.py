    #NAME - ADITYA SHIVAJI PATIL
#STUDENT ID-1001995431
# Reference - https://realpython.com/python-sockets/
# Reference - https://www.tutorialspoint.com/python/os_listdir.htm
# Reference - https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
# Reference - http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
import socket
import os #for getting details of directories
import glob
import time
import pickle #serializing and deserializing with the Python pickle module.
import shutil
from pathlib import Path
import threading
import datetime

final_files=[]
final_size=[]
final_time=[]
temp_files=[]
file_s1 = []
local_t1 = []
lock=[]
modifiedfile=[]
lockthreads=[]


i =0
def ServerB():
    HOST1 = '10.199.144.217' #server_b connection till line 26
    PORT1 = 3001
    time.sleep(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST1,PORT1))
    data = s.recv(1024)
    print(data.decode("utf-8"))
    info = s.recv(2048)
    all = pickle.loads(info)
    list_of_files2=[]
    file_size2=[]
    local_time2=[]
    for f in range(len(all)):
        fb,sb,tb=all[f]
        list_of_files2.append(fb)
        file_size2.append(sb)
        local_time2.append(tb)

    sorted_files=[]
    sorted_time=[]
    sorted_size=[]
    p='C:/Users/adity/OneDrive/Desktop/submit/directory_a'
    list_of_files=os.listdir(p)#server_a files
    list_of_files= sorted( list_of_files, key = os.path.getmtime)#sorting with key-modification_time
    for files in list_of_files:
        path=str(files)
        file_size = os.path.getsize(path)
        file_s1.append(str(file_size))#changing type to string
        modification_time = os.path.getmtime(path)#getting modification_time of files
        local_time = time.ctime(modification_time)# according to system time
        local_t1.append(str(local_time))
        print(files,file_size,"bytes",local_time)


    i=0
    check = list_of_files+list_of_files2#full list of files from server_a+server_b
    for x in range(len(check)):
        final_files.append(str(check[x]))#full list of files from server_a+server_b to check and get index for size and time later for sorting
        sorted_files.append(str(check[x]))#full list of files from server_a+server_b which will be sorted
        i=i+1

    temp_files=sorted_files
    final_size=file_s1+file_size2 #full list of file size from server_a+server_b

    final_time=local_t1+local_time2#full list of file time from server_a+server_b


    i=0


    sorted_files.sort()#sorting file names list

    i=0
    j=0
    #sorting all files_size and modification_time according to file name
    for x in range(len(final_files)):
        for f in range(len(final_files)):
            if sorted_files[x]==final_files[f]:
                sorted_size.append(str(final_size[f]))
                sorted_time.append(str(final_time[f ]))


def Update(): # Function used for checking updates made in directories
    path='C:/Users/adity/OneDrive/Desktop/submit/directory_a'
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
                    if fa == fb: #Check if name of files same
                        check=10
                if check == 0:
                    added.append(fa) # add the file name in added list
                check=0
        if len(before)>len(after): # if updated list smaller
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

        if len(added)!=0 or len(removed)!=0:
            time.sleep(1)
        before=after
        added.clear()
        removed.clear()
        Sync()

def Sync(): # Sync the files in both directories
    src = 'C:/Users/adity/OneDrive/Desktop/submit/directory_a'
    dest ='C:/Users/adity/OneDrive/Desktop/submit/directory_b'
    aa=os.listdir(src)#dir_a
    bb=os.listdir(dest)#dir_b
    check=0

    for a in aa:#dir_a
        if a not in lock:
            for b in bb:#dir_b
                if a==b: # if name of files a and b are same
                    check=10
                    fa = 'C:/Users/adity/OneDrive/Desktop/submit/directory_a/{}'.format(a)
                    fb = 'C:/Users/adity/OneDrive/Desktop/submit/directory_b/{}'.format(b)
                    time1 = time.ctime(os.path.getmtime(fa))# get modification time of file common file
                    time2 = time.ctime(os.path.getmtime(fb))# get modification time of file common file
                    if time1==time2 : #if time of files same ignore
                        break
                    if time1>time2 :#if time of file a > time of file b(latest modified=a)
                        shutil.copy2(os.path.join(src,a),dest)
                    if time1<time2 :#if time of file b > time of file a(latest modified=b)
                        shutil.copy2(os.path.join(dest,b),src)

            if check == 0:
                shutil.copy2(os.path.join(src,a),dest) #if files name different then send file to dest
            check=0

    check=0
    for b in bb:
        for a in aa:
            if a==b:
                check=10
                break
        if check == 0:
            shutil.copy2(os.path.join(dest,b),src) #if files name different then send file to dest
        check=0
#continuously checks for updates to a locked file
def lockfunc(lf):
    before=[]
    after=[]
    added=[]
    removed=[]

    n=0
    before = 'C:/Users/adity/OneDrive/Desktop/submit/directory_b/{}'.format(lf)
    time1 = time.ctime(os.path.getmtime(before))
    while 1:
        after = 'C:/Users/adity/OneDrive/Desktop/submit/directory_b/{}'.format(lf)
        time2 = time.ctime(os.path.getmtime(after))

        if time2 != time1:#if modified then go inside loop
            temp=lf.split('.')
            x=temp[0]+str(n)+"."+temp[1]
            dest = 'C:/Users/adity/OneDrive/Desktop/temp/{}'.format(x)#s
            modifiedfile.append(x)#appending the temporary file names
            shutil.copy2(after,dest)#copying the temporary file in temp folder
            n+=1

        time1=time2

#unlock file using queue - popfiles
def unlockfunc(unlock):
    popfiles=[]
    for f in modifiedfile:
        fsplit=f.split('.')#getting name of file
        first=fsplit[0][:-1]
        last=fsplit[1]
        fname = first+'.'+last
        unlocksplit=unlock.split('.')
        if unlock==fname:
            popfiles.append(f)
    for f in range(len(popfiles)):
        s=popfiles.pop(0)
        srcu='C:/Users/adity/OneDrive/Desktop/temp/{}'.format(s)#s
        destu='C:/Users/adity/OneDrive/Desktop/submit/directory_a/{}'.format(unlock)
        shutil.copy2(srcu,destu)
        time.sleep(2)#put 16 for observing changes in queued manner
        location="C:/Users/adity/OneDrive/Desktop/temp"
        path = os.path.join(location, s)
        #os.remove(path)#deleting the temp files
        modifiedfile.remove(s)
    lock.remove(unlock)


#client handled using a thread
def Client():
    time.sleep(1)
    lockcounter=0
    HOST = '10.199.144.217' # is the standard IPv4 address for the loopback interface
    PORT = 3000
    status=[]
    jj=20
    for i in range(jj):
        status.append("Unlocked")
    #socket.socket - creates a socket obect  AF_INET- socket family(ipv4) , SOCK_STREAM- type of socket(TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen()
    while True:
        n=[]
        i=1
        Sync()
        #sorted_files=[]#for files
        sorted_time=[]#for file modified time
        sorted_size=[]# for file size
        fil=os.listdir()#server_a files
        #sorted_files= sorted( sorted_files, key = os.path.getmtime)#sorting with key-modification_time
        sorted_files=sorted(fil)
        for files in sorted_files:
            n.append(str(i))
            i=i+1
            path=str(files)
            file_size = os.path.getsize(path)
            sorted_size.append(str(file_size))#changing type to string
            modification_time = os.path.getmtime(path)#getting modification_time of files
            local_time = time.ctime(modification_time)# according to system time
            sorted_time.append(str(local_time))
        conn, addr = s.accept()
        print('connected by', addr)
        conn.send(bytes("Welcome to the server1!","utf-8"))
        print("")
        cour=0
        #for sending a single list all- contains index, file name, file size, file modification time
        all=[]
        for q in range(len(sorted_files)):
            if sorted_files[cour] in lock:
                qtemp = n[cour]+" "+sorted_files[cour]+" "+sorted_size[cour]+" "+sorted_time[cour]+" Locked"
            else:
                qtemp = n[cour]+" "+sorted_files[cour]+" "+sorted_size[cour]+" "+sorted_time[cour]
            all.append(qtemp)
            cour=cour+1
        info=pickle.dumps(all)
        conn.send(info)
        inp=conn.recv(1024)
        userinput=inp.decode('UTF-8')
        #l_u=userinput[0:1]
        command=userinput.split(' ',1)
        l_u=command[0]
        #indextol_u=int(userinput[1:])
        indextol_u=int(command[1])
        #chcecking user input input if lock or unlock
        if l_u == "lock":
            lock.append(sorted_files[indextol_u-1])
            templockfile=sorted_files[indextol_u-1]
            #dynamic multithreading for each locked file
            lockthreads.append(threading .Thread(target=lockfunc,args=(templockfile,)))
            tt=lockthreads[lockcounter]
            tt.start()#starting thread
            lockcounter=lockcounter+1
            print(sorted_files[indextol_u-1]," Locked")
        if l_u == "unlock":
            unlockfunc(sorted_files[indextol_u-1])
            print(sorted_files[indextol_u-1]," Unlocked")



if __name__ == '__main__':
    ServerB() #connects to ServerB
    thread1= threading .Thread(target=Update,args=()) #for updating adn Sync
    thread2= threading .Thread(target=Client,args=()) #for taking care of client
    thread1.start()
    thread2.start()
