import tkinter as tk                # python 3
from tkinter import Image, Label, mainloop, ttk
from tkinter import messagebox
from tkinter.constants import CENTER
from tkinter.messagebox import showinfo
from tkinter import font as tkfont
from typing import Container
from GetAPI import *
import sys
import json
import socket
import threading
import time

HOST = "127.0.0.1"   #Tạo server với IP lấy từ máy này bằng cách loopback lại máy này    
# Thiết lập port lắng nghe, không để nhỏ hơn 1024, tránh bị trùng với port trên máy tính, đồng bộ với bên client
PORT = 7654
FORMAT = "utf8"
HEADER = 64

# Các message gửi sang client sẽ được liệt kê dưới đây
Okay = "oke"            # Đã nhận được message
FNF = "FileNotFound"
UNF = "UsernameNotFound"
wrongPass = "wrongPassword"
sendAgain = "sendAgain"
valUser = "ValidUsername"
NotRecv = "NotReceive"

# Các message được client gửi tới sẽ được liệt kê dưới đây
Client_exit = "clientexit"
Client_enter= "cliententer"
Close_Server = "close"

#############
SIGNIN = 'SIGNIN'
SIGNUP = 'SIGNUP'

Clients = []

# tạo socket SERVER, với địa chỉ IPv4, giao thức TCP
try:
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("FAILED TO CREATE SERVER !!")
    sys.exit();
SERVER.bind((HOST, PORT))    # Gán địa chỉ (HOST, PORT) cho SERVER

class AppServer(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Tạo WINDOW cho APP 
        self.title_font = tkfont.Font(family = 'Helvetica', size = 32, weight = "bold", slant = "italic")
        self.title("SEARCHING APP")
        sizex = 710
        sizey = 400
        posx  = 100
        posy  = 100
        self.geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
        self.resizable(width = False, height = False)

        self.isEndServer = 0
        # container chứa 3 frame của APP: 1. SearchingPage, 2. SearchingDay, 3. SearchingCurrency
        container = tk.Frame(self)
        container.pack(side = "top")
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # Tạo frames cho container
        self.frames = {}
        for F in (StartPage, Server):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame

            # Đặt tất cả các frame page ở cùng một vị trí trên Window của APP
            frame.grid(row = 0, column = 0, sticky = "nsew")

        # Hiện SearchingPage trước tiên
        self.showFrame("StartPage")

    def EndServer(self):
        if self.isEndServer == 0:
            messagebox.showwarning("Exit","SERVER CLOSED !!")
            for X in Clients:
                X.close()
            self.isEndServer = 1
            self.destroy()
            SERVER.close() 

    # Hàm showFrame để hiện các frame page đã lưu trong self.frames
    def showFrame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

# Page tra cứu
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Là một frame WINDOW của APP nên gọi lại controller (self = tk.Tk)
        self.controller = controller
        label = tk.Label(self, text = "SERVER", font = controller.title_font)
        label.pack(side = "top", pady = 100)

        self.title_font = tkfont.Font(family = 'Helvetica', size = 14, weight = "bold", slant = "italic")
        ConnectServer = tk.Button(self, text = "START SERVER", padx = 100, pady = 50, font = self.title_font,
                            command = lambda: controller.showFrame("Server"))

        ConnectServer.pack()

class Server(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.accounts = []
        self.connections = self.Connect()
        self.tile_font = tkfont.Font(family = 'Helvetica', size = 14, weight = "bold", slant = "italic")
        self.miniFont = tkfont.Font(family = 'Helvetica', size = 10, weight = "bold", slant = "italic")
        
    #---------------------------------------------
    
    # đưa qua file json
    def updateAPIper30(self): 
        while True:
            # cursor chứa dữ liệu của giá trị đồng tiền
            getAPIfromWeb()
            time.sleep(1800)    #Nghỉ 30p cho lần lặp kế tiếp
    
    #-----------------------------------------------

    def SignIn(self, conn: socket):
        #server nhận username + password  
    
        username = conn.recv(1024).decode(FORMAT)
        conn.sendall(Okay.encode(FORMAT))
        password = conn.recv(1024).decode(FORMAT)

        try:
            with open("userData.json",'r') as file:
                file_data = json.load(file)
            if username not in file_data:
                conn.sendall(UNF.encode(FORMAT))
            else:
                for user in file_data:
                    if username == user:
                        if file_data[user]["password"] != password:
                            conn.sendall(wrongPass.encode(FORMAT))
                            return
                        else:
                            conn.sendall(Okay.encode(FORMAT))
                            return

        except FileNotFoundError:
            conn.sendall(FNF.encode(FORMAT))        #Send File Not Found (nghĩa là chưa có file User để mà login)
            return

    #----------------------------------------------

    def SignUp(self, conn: socket):
        #server nhận username + password + confirm password

        username = conn.recv(1024).decode(FORMAT)
        conn.sendall(Okay.encode(FORMAT))
        password = conn.recv(1024).decode(FORMAT)
        conn.sendall(Okay.encode(FORMAT))
        content = {
                username: {
                    "password": password
                }
            }
        
        try:
            with open("userData.json",'r') as file:
                file_data = json.load(file)        
            if username in file_data:
                conn.sendall(valUser.encode(FORMAT))
            else:
                file_data.update(content)
                with open("userData.json", "w") as outfile:
                    json.dump(file_data, outfile, indent = 4)
                conn.sendall(Okay.encode(FORMAT))

                self.showAccount()

                return

        except FileNotFoundError:                       #Trường hợp ko có file userData thì ta tạo file mới và lưu
            with open("userData.json", "w") as outfile:
                json.dump(content, outfile, indent = 4)
            conn.sendall(Okay.encode(FORMAT))           #Send Okay, đăng kí thành công
            
            self.showAccount()
            
            return
        
    #----------------------------------------------

    def connClient(self, conn: socket, addr):
        try:
            msg = None
            while (msg != Client_exit and self.controller.isEndServer == 0):
                msg = conn.recv(1024).decode(FORMAT)        
                if (msg == SIGNIN):
                    Server.SignIn(self, conn)
                elif (msg == SIGNUP):
                    Server.SignUp(self, conn)
                elif (msg == Client_enter):
                    conn.sendall(Okay.encode(FORMAT))

            tk.Label(self.myframe, text = "CLIENT " + str(addr) + " CLOSE !!", font = self.miniFont).grid(column = 0, sticky="nw")
            conn.close()
            Clients.remove(conn)
        except:
            return

    def init_RunThread(self):
        #---------------------------------------------
        #số luồng của server (số client mà server có thể trao đổi trong cùng 1 lúc)
        SERVER.listen(1)
        while (True):
            try:
                conn, addr = SERVER.accept()
                Clients.append(conn)
                tk.Label(self.myframe, text = "CLIENT " + str(addr) + " CONNECTED !!", font = self.miniFont).grid(column = 0, sticky= "nw")
                    
                # gọi đa luồng cho Server
                thread = threading.Thread(target = self.connClient, args = (conn, addr))
                thread.daemon = True
                thread.start()

            except:
                if self.controller.isEndServer == 0:
                    self.controller.isEndServer = 1
                    messagebox.showwarning("Exit","SERVER CLOSED !!")
                    for X in Clients:
                        X.Close()
                    SERVER.close()

    def Connect(self):  
        # Vẽ frame chứa các button 
        self.mycanvas = tk.Canvas(self, height = 360, width = 280)
        self.mycanvas.grid(row = 0, column = 0, sticky= "nw")

        # Tạo thanh cuộn cho frame chứa button
        yscrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.mycanvas.yview)
        yscrollbar.grid(row = 0, column = 0, sticky = "ne", rowspan = 100, ipady = 158)

        self.mycanvas.configure(yscrollcommand = yscrollbar.set)
        self.mycanvas.bind('<Configure>', lambda e: self.mycanvas.configure(scrollregion = self.mycanvas.bbox('all')))

        self.myframe = tk.Frame(self.mycanvas)
        self.mycanvas.create_window((0,0), window = self.myframe, anchor = "nw")

        self.showAccount()

        # Button back về Searching Page 
        button = tk.Button(self, text = "END SERVER", command = lambda: self.controller.EndServer(),
                                     height = 2, width = 40)
        button.grid(row = 1, column = 0)
        
        startServer = threading.Thread(target = self.init_RunThread)
        updateCursor = threading.Thread(target = self.updateAPIper30)
        startServer.daemon = True
        updateCursor.daemon = True
        startServer.start()    
        updateCursor.start()
        
    # Hàm show Currency khi click vào button có mang tiền tệ
    def showAccount(self):
        # Tạo column cho table
        columns = ("username", "password")

        # Tạo table
        table = ttk.Treeview(self, columns = columns, show = 'headings', height = 17)
        
        # # Định dạng kích thước mỗi cột cho table
        # table.column('username', width = 100)
        # table.column('password', width =  100)

        # Tạo heading cho bảng tra cứu (table)
        table.heading('username', text = 'USERNAME', anchor = CENTER)
        table.heading('password', text = 'PASSWORD', anchor = CENTER)
        try:
            with open("userData.json",'r') as file:
                file_data = json.load(file)
            for n in file_data:
                self.accounts.append((n, file_data[n]['password']))
        except:
            nUser = "None"
            nPass = "None"
            self.accounts.append((nUser, nPass))

        # Thêm phần nội dung vào table
        for account in self.accounts:
            table.insert('', tk.END, values = account)

        # Tạo table và grid vào frame
        table.bind('<<TreeviewSelect>>', self.item_selected)
        table.grid(row = 0, column = 1, sticky = "ne")

        # Tạo và grid thanh cuộn cho table
        scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = table.yview)
        table.configure(yscroll = scrollbar.set)
        scrollbar.grid(row = 0, column = 2, sticky = "ns")

        self.table = table
        self.accounts.clear()

    def item_selected(self, event):
        for selected_item in self.table.selection():
            # select item trong chuỗi item đã lưu 
            item = self.table.item(selected_item)
            record = item['values']
            # show thông tin item vào table
            showinfo(title = 'Information', message = ','.join(record))   

app = AppServer()

def Close():
    if messagebox.askokcancel("Exit", "Wanna quit bruh?"):
        app.EndServer()

app.protocol("WM_DELETE_WINDOW", Close)
app.mainloop()

        