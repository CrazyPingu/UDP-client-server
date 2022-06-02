#!/usr/bin/python3

from socket import *
from os.path import *
from sys import *

def send_file(message):
    s.sendto(str.encode(message),addr)
    f=open(str.encode(message),"rb")
    data = f.read(buf)
    while (data):
        if(s.sendto(data,addr)):
            data = f.read(buf)
    f.close()

def receive_file(data):
    f = open(data,'wb')
    s.settimeout(4)    
    try:
        while True:
            data, address = s.recvfrom(buf)
            f.write(data)
    except timeout:
        pass
    finally:
        f.close()
        print ("File received")

def get_filename(receive_data:str):
    return receive_data.split()[0] if receive_data.split()[0] != "put" else receive_data.split()[1]

def obtain_list():
    data, address = s.recvfrom(buf)
    list_of_file = ""
    if data.decode() == "0":
        print("The server does not have any file")
    else:
        for i in range(int(data)):
            data, address = s.recvfrom(buf)
            list_of_file += data.decode() + " | "
        print (list_of_file[:len(list_of_file)-2])

def print_command():
    print("list to get the list of the files that are in the server")
    print("put filename where filename is the name of the file you want to send to the server")
    print("get filename where filename is the name of the file you want to get")
    print("help to obtain the list of command")
    print("close to close the connection")

host = "localhost"
port = 9999
buf = 1024
addr = (host,port)
s = socket(AF_INET,SOCK_DGRAM)
print("Type help to check the commands")

while True:
    s.settimeout(None)
    message = input("Do the thing: ")
    if message == "close":
        s.sendto(message.encode(), addr)
        s.close()
        print("Closing the client")
        exit(0)
    elif len(message.split()) > 2:
        print("Usa solo 2 comandi")
    elif "get" in message:
        s.sendto(message.encode(), addr)
        data,addr = s.recvfrom(buf)
        if data.decode() == "The file does not exist":
            print("The file does not exist")
        else:
            receive_file(data.decode())
    elif "put" in message:
        if exists(get_filename(message)):
            s.sendto(message.encode(), addr)
            print(f"Sending {get_filename(message)}")
            send_file(get_filename(message))
            confirm, address = s.recvfrom(buf)
            print(confirm.decode())
        else:
            print("The file does not exist")
    elif message == "list":
        s.sendto(message.encode(), addr)
        obtain_list()
    elif message == "help":
        print_command()
    else:
        print("Command does not exist")


