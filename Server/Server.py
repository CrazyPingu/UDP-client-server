from socket import *
import os
from sys import *
import threading

def send_file(message):
    s.sendto(str.encode(message),addr)
    f=open(str.encode(message),"rb")
    data = f.read(buf)
    while (data):
        if(s.sendto(data,addr)):
            data = f.read(buf)
    f.close()

def receive_file():
    data = s.recv(buf)
    f = open(data,'wb')
    data = s.recv(buf)
    try:
        while data:
            f.write(data)
            s.settimeout(4)    
            data, address = s.recvfrom(buf)
    except timeout:
        pass
    finally:
        f.close()
        print ("File received")
        s.sendto(str.encode("File uploaded correctly"),addr)

def get_filename(receive_data:str, avoid):
    return receive_data.split()[0] if receive_data.split()[0] != avoid else receive_data.split()[1]

def command_to_do():
    if "get" in receive_data:
        if os.path.exists(get_filename(receive_data, 'get')) and get_filename(receive_data, 'get') != "Server.py":
            print(f"Sending {get_filename(receive_data,'get')}")
            send_file(get_filename(receive_data, "get"))
        else:
            s.sendto(str.encode("The file does not exist"),addr)
    elif "put" in receive_data:
        print(f"Receiving {get_filename(receive_data, 'put')}")
        receive_file()
    elif receive_data == "list":
        list_to_send = os.listdir()
        list_to_send.remove('Server.py')
        print("Sending list of the file")
        for file_name in list_to_send:
            s.sendto(file_name.encode(), addr)

host = 'localhost'
port = 9999
buf = 1024
addr = (host, port)
s = socket(AF_INET,SOCK_DGRAM)
s.bind(addr)

while True:
    s.settimeout(None)
    data,addr = s.recvfrom(buf)
    receive_data = data.decode('utf-8')
    thread = threading.Thread(target=command_to_do)
    thread.start()
    thread.join()
    