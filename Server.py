from ctypes import FormatError
import sys
import socket
from tkinter import *
import threading
import pyodbc

# Thiết lập địa chỉ, về sau sẽ mở rộng bằng cách cho client tự nhập địa chỉ IP của server để kết nối
HOST = socket.gethostbyname(socket.gethostname())         
# Thiết lập port lắng nghe, không để nhỏ hơn 1024, tránh bị trùng với port trên máy tính
PORT = 7654
FORMAT = "utf8"
HEADER = 64

# tạo socket SERVER, với địa chỉ IPv4, giao thức TCP
try:
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("FAILED TO CREATE SERVER !!")
    sys.exit();
SERVER.bind((HOST, PORT))    # Gán địa chỉ (HOST, PORT) cho SERVER

# connect đến SQL ----------------------------------
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                            SERVER=ADMIN\YAKHIM;\
                            Database=Socket_Account;\
                            UID=YaKhim; PWD=aimanho1;')
cursor = connection.cursor()

#---------------------------------------------

def LogIn(conn: socket):
    #server nhận username + password  
    username = conn.recv(1024).decode(FORMAT)
    cursor.execute("select * from Account where username = ?", username) 
    user = cursor.fetchall
    if (user == []):
        print('INVALID ACCOUNT')
        conn.sendall('INVALID ACCOUNT'.encode(FORMAT))
    else:
        #servet phản hồi lại client khi nhận được username hợp lệ
        conn.sendall(username.encode(FORMAT))
        pwd = conn.recv(1024).decode(FORMAT)

        # Lấy dữ liệu từ SQL
        cursor.execute("select pass from Account where username = ?", username)
        password = cursor.fetchone()
        # Vì khi SQL trả về thì pass = ('1', )
        true_password = password[0]
        if (pwd == true_password):
            print('LOGIN SUCCESSFULL !!')
            conn.sendall('TRUE'.encode(FORMAT))
        else:
            print('PASSWORD OR ACCOUNT IS INCORRECT')
            conn.sendall('FALSE'.encode(FORMAT))

#----------------------------------------------

def SignUp(conn: socket):
    # Nhận thông tin của username
    username = conn.recv(1024).decode(FORMAT)
    # Tìm kiếm thông tin của username trong Account
    cursor.execute("select * from Account where username = ?", username) 
    user = cursor.fetchall
    # Nếu có thì sẽ gửi INVALID về client
    note = None
    if (user != [] ):
        note = 'INVALID'
        conn.sendall(note.encode(FORMAT))
    # Nếu không thì gửi ACCEPT về để client tiếp tục thực hiện
    else:
        note = 'ACCEPT'
        conn.sendall(note.encode(FORMAT))
        pwd = conn.recv(1024).decode(FORMAT)
        print(username, " ",pwd)
        # Sau khi nhận password từ Client thì Server sẽ push vào Account trong SQL
        cursor.execute("insert Account values (? , ?)", username, pwd)

        # Thông báo cho Client và print ra ngoài Server
        notify = 'CREATING ACCOUNT IS SUCCESSFULL !!'
        print(notify)
        conn.sendall(notify.encode(FORMAT))
    
#----------------------------------------------

LOGIN = 'LOGIN'
SIGNUP = 'SIGNUP'

# Hàm để connect giữa Client và Server
def connClient(conn: socket, nThread, sent):
    msg = None
    while (msg != "END"):
        msg = conn.recv(1024).decode(FORMAT)
        print("Client ", nThread, ": ", msg)
       
        if (msg == LOGIN):
            LogIn(conn)
        if (msg == SIGNUP):
            SignUp(conn)

    print("CLIENT", nThread, "CLOSE !!")
    conn.close()


SERVER.listen(1)             # Thiết lập tối đa một kết nối, bắt đầu TCP listen
print("Waiting for client to connect...")

def init_RunThread(conn, addr):
    #---------------------------------------------
    #số luồng của server (số client mà server có thể trao đổi trong cùng 1 lúc)
    nThread = 0
    sent = None
    while (nThread < 1):
        try:
            conn, addr = SERVER.accept()
            print("CLIENT ", nThread, addr, "CONNECTED !!")
                
            # gọi đa luồng cho Server
            thread = threading.Thread(target = connClient, args = (conn, nThread, sent))
            thread.daemon = False
            thread.start()

        except KeyboardInterrupt:
            print("ERROR !!")
            SERVER.close()
        nThread += 1 
            
    # # Để finaly không được :)
    if (input() == "END"):
        print("SERVER DEAD !!")
        SERVER.close()
        connection.close()
        conn.close()