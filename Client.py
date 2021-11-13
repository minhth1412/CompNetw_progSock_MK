import sys
import socket
import tkinter as tk
import threading
import json
from tkinter import messagebox
from tkinter import ttk

HOST = "127.0.0.1"
# Đồng nhất port với bên server
PORT = 7654
SERVER_addr = (HOST, PORT)
FORMAT = "utf8"
HEADER = 64

################################


################################


# initialize socket CLIENT
try:
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Failed to create Client!")
    sys.exit();

CLIENT.connect(SERVER_addr)       # Kết nối tới SERVER

try:
    data = None
    while (data != "End"):
        data = input("Write sth: ")
        CLIENT.sendall(data.encode(FORMAT))
except:
    print("Server isn't responding!")
    CLIENT.close()
finally:
    CLIENT.close()