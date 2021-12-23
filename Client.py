import sys
import socket
import tkinter as tk
import threading
import pyodbc
from tkinter import messagebox
from tkinter import ttk

HOST = socket.gethostbyname(socket.gethostname())
# Đồng nhất port với bên server
PORT = 7654
SERVER_addr = (HOST, PORT)
FORMAT = "utf8"
HEADER = 64

# initialize socket CLIENT
try:
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("FAILED TO CREATE CLIENT !!")
    sys.exit();

#-------------------------------------------------
# Đăng nhập
def LogIn(CLIENT):
    # Nhập username và password
    username = input("USER: ")  
    pwd = input("PASS: ")

    # Client gửi thông tin về server để kiểm tra thông tin
    CLIENT.sendall(username.encode(FORMAT))
    # lệnh client.recv() để client gửi tuần tự username - pass về cho server
    checkingUser = CLIENT.recv(1024)
    if (checkingUser != 'INVALID ACCOUNT'):
        CLIENT.sendall(pwd.encode(FORMAT))
        # CLient nhận phản hồi từ server tài khoản có đúng hay không
        check = CLIENT.recv(1024)
        if (check == 'FALSE'):
            print('PASSWORD OR ACCOUNT IS INCORRECT')

#----------------------------------------------------
# Đăng ký
def SignUp(CLIENT):
    # Client nhập username + password

    username = input("USER: ")

    # Client gửi thông tin Username qua cho Server kiểm tra
    CLIENT.sendall(username.encode(FORMAT))

    # Server kiểm tra và phản hồi lại Client 
    checkingUser = CLIENT.recv(1024)

    # Kiểm tra thông tin của username
    if (checkingUser == 'INVALID'):
        print('INVALID ACCOUNT !!')
        return   
    else:   
        pwd = input("PASS: ") 
        CLIENT.sendall(pwd.encode(FORMAT))
        # Client thông báo cho người dùng
        notify = CLIENT.recv(1024).decode(FORMAT)
        print(notify)           

#-----------------------------------------------

LOGIN = 'LOGIN'
SIGNUP = "SIGNUP"

# Đưa dòng CLIENT.connect vào try để khi chạy client trước server thì end nếu không sẽ bị lỗi
try: 
    CLIENT.connect(SERVER_addr)       # Kết nối tới SERVER
    print("CLIENT ADDRESS: ", CLIENT.getsockname())
    msg = None
    while (msg != "END"):
        msg = input("Talk to server: ")
        CLIENT.sendall(msg.encode(FORMAT))
        #receive = CLIENT.recv(1024).decode(FORMAT)
        #print("Server respone: ", receive)
        #if (receive == "END"):
        #    msg = receive
        if (msg == LOGIN):
            LogIn(CLIENT)
        if (msg == SIGNUP):
            SignUp(CLIENT) 
except:
    print("SERVER ISN'T RESPONDING!")
    CLIENT.close()
finally:
    print("CLIENT CLOSED !!")
    CLIENT.close()