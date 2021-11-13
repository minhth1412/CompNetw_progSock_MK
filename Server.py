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

# tạo socket SERVER, với địa chỉ IPV4, giao thức TCP
try:
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Failed to create Server!")
    sys.exit();

SERVER.bind((HOST, PORT))    # Gán địa chỉ (HOST, PORT) cho SERVER
SERVER.listen(1)     # Thiết lập tối đa một kết nối, bắt đầu TCP listen
print("Waiting for client to connect...")


conn, addr = SERVER.accept()     # thiết lập kết nối với Client

try:
    data = None
    while (data != "End"):
        data = conn.recv(1024).decode(FORMAT)
        print("client ", addr, "says", data)
        #if not data: break
except KeyboardInterrupt:
    print("Error!")
    SERVER.close()
finally:
    SERVER.close()
    print("The end!")