import sys
import socket
import tkinter as tk
import threading
import json
from tkinter import messagebox
from tkinter import ttk

#HOST = socket.gethostbyname(socket.gethostname())
HOST = "127.0.0.1"
# Đồng nhất port với bên server
PORT = 7654
SERVER_addr = (HOST, PORT)
FORMAT = "utf8"
HEADER = 64

################################

##client nhập username + password
#username = input("USER: ")
#pass = input("PASS: ")
#client.sendall(username.encode(FORMAT))
##lệnh client.recv() để client gửi tuần tự username - pass về cho server
#client.recv(1024)
#client.sendall(pass.encode(FORMAT))

################################

# initialize socket CLIENT
try:
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Failed to create Client!")
    sys.exit();

# Đưa dòng CLIENT.connect vào try để khi chạy client trước server thì end nếu không sẽ bị lỗi
try:
    CLIENT.connect(SERVER_addr)       # Kết nối tới SERVER
    print("Client address: ", CLIENT.getsockname())
    data = None
    while (data != "END"):
        data = input("Talk to server: ")
        CLIENT.sendall(data.encode(FORMAT))      
except:
    print("Server isn't responding!")
    CLIENT.close()
finally:
    print("Client closed !!")
    CLIENT.close()