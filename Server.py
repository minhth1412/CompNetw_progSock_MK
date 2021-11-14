import sys
import socket
import tkinter as tk
import threading
import json
from tkinter import ttk

# Thiết lập địa chỉ, về sau sẽ mở rộng bằng cách cho client tự nhập địa chỉ IP của server để kết nối
# HOST = socket.gethostbyname(socket.gethostname())
HOST = "127.0.0.1"          
# Thiết lập port lắng nghe, không để nhỏ hơn 1024, tránh bị trùng với port trên máy tính
PORT = 7654
FORMAT = "utf8"
HEADER = 64

# Hàm để connect giữa Client và Server
def connClient(conn: socket, nThread):
    data = None
    #msg = None
    while (data != "END"):
        data = conn.recv(1024).decode(FORMAT)
        print("Client ", nThread, ": ", data)  
        ## Server sẽ phản hồi lại client (khi cần)  
        #data = input("Server response: ")
        #conn.sendall(data.encode(FORMAT))          
        #if not data: break
    conn.close()

# tạo socket SERVER, với địa chỉ IPv4, giao thức TCP
try:
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Failed to create Server!")
    sys.exit();

SERVER.bind((HOST, PORT))    # Gán địa chỉ (HOST, PORT) cho SERVER
SERVER.listen(1)             # Thiết lập tối đa một kết nối, bắt đầu TCP listen
print("Waiting for client to connect...")

################################

##server nhận username + password
#username = conn.recv(1024).encode(FORMAT)
##servet phản hồi lại client khi nhận được username
#conn.sendall(username.encode(FORMAT))
#pass = con.recv(1024).encode(FORMAT)

################################

#số luồng của server (số client mà server có thể trao đổi trong cùng 1 lúc)
nThread = 0
while (nThread < 3):
    try:
        conn, addr = SERVER.accept()     # thiết lập kết nối với Client
        print("Client ", nThread, addr, "connected !!")
        # gọi đa luồng cho Server
        thread = threading.Thread(target = connClient, args = (conn, nThread))
        thread.daemon = False
        thread.start()
       
    except KeyboardInterrupt:
        print("ERROR !!")
        SERVER.close()
       
    nThread += 1   

# Để finally không được :) 
print("SERVER DEAD !!")		# :))
SERVER.close()
    
