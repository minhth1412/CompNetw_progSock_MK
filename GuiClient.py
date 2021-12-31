import sys
import socket
from tkinter import Tk
import tkinter as tk                # python 3
from tkinter import font as tkFont
from GetAPI import *
from tkinter import messagebox
from SearchingPage import *

# Remember to handle message send to server between two comment like the one below:
##################
#....................                   /message
##################

PORT = 7654
FORMAT = "utf8"
HEADER = 64

# Các message gửi sang server sẽ được liệt kê dưới đây
Client_exit = "clientexit"
Client_enter= "cliententer"
Close_Server = "close"

# Các message được server gửi tới sẽ được liệt kê dưới đây
Okay = "oke"            # Đã nhận được message
FNF = "FileNotFound"
UNF = "UsernameNotFound"
wrongPass = "wrongPassword"
sendAgain = "sendAgain"
valUser = "ValidUsername"

SIGNIN = 'SIGNIN'
SIGNUP = 'SIGNUP'

try:
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("FAILED TO CREATE CLIENT !!")
    sys.exit();

class AppClient(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Tạo WINDOW cho AppClient
        self.title("CLIENT")
        sizex = 400
        sizey = 350
        posx  = 100
        posy  = 100
        self.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
        self.resizable(width = False, height = False)
        self.title_font = tkFont.Font(family = 'Helvetica', size = 32, weight = "bold", slant = "italic")
        self.miniFont = tkFont.Font(family = 'Helvetica', size = 14, slant = "italic")
        self.isClientClose = 0      #  0 = chua dong, 1  = dong roi

        # container chứa 3 frame của AppClient: 1. StartPage, 2. SignIn, 3. SignUp
        container = tk.Frame(self)
        container.pack(side = "top")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # Tạo frames cho container, gán nhãn tương đương với tên container
        self.frames = {}
        for F in (HomePage, StartPage, SignIn, SignUp):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame

            # Đặt tất cả các frame page ở cùng một vị trí trên Window của AppClient
            frame.grid(row = 0, column = 0, sticky = "nsew")
        self.showFrame("HomePage")
    
    def checkIP(self, ip):
        HOST = "127.0.0.1"
        # HOST = str(ip.get())
        
        SERVER_addr = (HOST, PORT) 
        try: 
            CLIENT.connect(SERVER_addr)                     # Kết nối tới SERVER
            CLIENT.sendall(Client_enter.encode(FORMAT))     # Gửi thông tin cho SERVER là đã kết nối
            CLIENT.recv(1024).decode(FORMAT)
            self.showFrame("StartPage")                     # Vào trang Start  
            CLIENT.settimeout(5)                            # Chờ phản hồi trong 5s, nếu ko phản hồi thì hiện thông báo dưới
        except:
            messagebox.showinfo("Notification!", "Can't connect to SERVER with given IP!")

    # Hàm hiện frame page_name đã lưu trong self.frames
    def showFrame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        ###################################################
        # Thống nhất phần kích cỡ của frame ở trong này
        ##########################################
        frame.tkraise()

    def End(self):
        if self.isClientClose == 0:
            try:
                CLIENT.sendall(Client_exit.encode(FORMAT))      #Gửi thông tin cho SERVER thông báo client đã đóng
                if messagebox.askokcancel("Exit", "Wanna quit bruh?"):
                    self.isClientClose = 1
                else:
                    return
            except:
                if messagebox.askokcancel("Exit", "Wanna quit bruh?"):
                    self.isClientClose = 1
                else:
                    return
            finally:
                self.destroy()
                CLIENT.close()
                #sys.exit()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.title_font = tkFont.Font(family = 'Helvetica', size = 14, weight = "bold", slant = "italic")
        # Hiện HomePage trước tiên
        label = tk.Label(self, text = "CLIENT", font = self.title_font)     
        ipLabel = tk.Label(self, text = "IP Server: ", font = self.title_font)
        IP = tk.StringVar()
        ipEntry = tk.Entry(self, textvariable = IP, font = self.title_font)
        notifyLabel = tk.Label(self, text = "")
        connect = tk.Button(self, text = "CONNECT", padx = 50, pady= 10, font= self.title_font, command = lambda: controller.checkIP(IP))

        for F in (label, ipLabel, ipEntry, notifyLabel, connect):
            F.pack()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text = "CLIENT", font = controller.title_font)
        label.pack(side = "top", pady = 20)

        self.title_font = tkFont.Font(family = 'Helvetica', size = 14, weight = "bold", slant = "italic")
        SignInButton = tk.Button(self, text = "SIGN IN", padx = 80, pady = 17, font = self.title_font,
                            command = lambda: controller.showFrame("SignIn"))
        SignUpButton = tk.Button(self, text = "SIGN UP", padx = 75, pady = 17, font = self.title_font,
                            command = lambda: controller.showFrame("SignUp"))
        EndClient = tk.Button(self, text = "END CLIENT", padx = 57, pady = 17, font = self.title_font,
                            command = lambda: controller.End())

        SignInButton.pack()
        SignUpButton.pack()
        EndClient.pack()
        
class SignIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        loginText_label = tk.Label(self, text = "SIGN IN CLIENT", font = self.controller.title_font, pady = 20)
        
        ##userName label
        self.title_font = tkFont.Font(family = 'Helvetica', size = 14, slant = "italic")
        usernameLabel = tk.Label(self, text ="Username: ", font = self.title_font)
        username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable = username, font = self.title_font)

        ##passWord Label
        passwordLabel = tk.Label(self, text = "Password", font = self.title_font )
        password = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable = password, show = '*', font = self.title_font)

        # Chạy hàm checkLogin và nếu success thì import và vào Searching không thì sẽ báo lỗi
        SignInButton = tk.Button(self, text = "Sign In", padx = 30, pady= 5, command = lambda: self.checkAccount(username, password))
        backButton = tk.Button(self, text = "BACK", padx = 35, pady= 5, command = lambda: controller.showFrame("StartPage"))
        
        for F in (loginText_label, usernameLabel, usernameEntry, passwordLabel, passwordEntry, SignInButton, backButton):
            F.pack()

    # Hàm check user bằng cách gửi thông tin cho server kiểm duyệt
    def checkAccount(self, username, password):
        Username = str(username.get())
        Password = str(password.get())

        username.set("")
        password.set("")

        if len(Username) == 0 or len(Password) == 0:
            messagebox.showwarning("Warning!!!", "Don't leave any field empty!")
            return

        # Gửi username và password đã nhập tới SERVER để check

        openSearchPage = 0
        try:
            CLIENT.sendall(SIGNIN.encode(FORMAT))
            CLIENT.sendall(Username.encode(FORMAT))
            CLIENT.recv(1024).decode(FORMAT)
            CLIENT.sendall(Password.encode(FORMAT))
            check = CLIENT.recv(1024).decode(FORMAT)

            if check == FNF:
                messagebox.showwarning("Warning!!!", "No data for login!")
            elif check == UNF:
                messagebox.showinfo("Notification!!!", "Invalid username!")
            elif check == wrongPass:
                messagebox.showinfo("Notification!", "Incorrect password!\nTry again!")
            elif check == Okay:
                messagebox.showinfo("Notification!", "Welcome back, bro!") 
                openSearchPage = 1
                if openSearchPage == 1:
                    run()
                    return

            CLIENT.settimeout(5)                            # Chờ phản hồi trong 5s, nếu ko phản hồi thì hiện thông báo dưới
            
        except:     #Không nhận lại phản hồi từ Server---------------------------- (quay lại chỗ nhập IP hử :)))
            messagebox.showwarning("Warning!!!", "Server corrupted!")
            ############################
            # Quay lại GUI nhập IP chỗ này nha ---------------
            ############################
            self.controller.showFrame("HomePage")   

class SignUp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.controller = controller

        loginText_label = tk.Label(self, text = "SIGN UP CLIENT", font = self.controller.title_font)      
        self.title_font = tkFont.Font(family = 'Helvetica', size = 14, slant = "italic")

        ##userName label
        usernameLabel = tk.Label(self, text = "Username: ", font = self.title_font)
        username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable = username, font = self.title_font, bg = "light yellow")

        ##passWord Label
        passwordLabel = tk.Label(self,text = "Password", font = self.title_font )
        password = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable = password, show = '*', font = self.title_font, bg = "light yellow")

        ## confirm_password
        confirm_passwordLabel = tk.Label(self,text = "Confirm Password", font = self.title_font )
        confirm_password = tk.StringVar()
        confirm_passwordEntry = tk.Entry(self, textvariable = confirm_password, show = '*', font = self.title_font)

        # Chạy hàm checkSignup và nếu success thì import và vào Searching không thì sẽ báo lỗi
        loginButton = tk.Button(self, text = "Sign Up", padx = 30, pady= 5, command = lambda: self.checkSignup(username, password, confirm_password) )            
        backButton = tk.Button(self, text = "BACK", padx = 35, pady= 5, command = lambda: controller.showFrame("StartPage"))
        
        for F in (loginText_label, usernameLabel, usernameEntry, passwordLabel, passwordEntry, confirm_passwordLabel, confirm_passwordEntry, loginButton, backButton):
            F.pack()
             
    def checkSignup(self, username, password, confirm_password):
        Username = str(username.get())
        Password = str(password.get())
        Cpassword = str(confirm_password.get())
        
        if len(Username) == 0 or len(Password) == 0 or len(Cpassword) == 0:
            messagebox.showwarning("Warning!!!", "Don't leave any field empty!")
        elif Cpassword != Password:
            messagebox.showinfo("Warning!!!", "Confirmed password don't match!")
        else:
            # Gửi lệnh đăng ký đến server
            
            try:
                CLIENT.sendall(SIGNUP.encode(FORMAT))

                CLIENT.sendall(Username.encode(FORMAT))
                CLIENT.recv(1024).decode(FORMAT)
                CLIENT.sendall(Password.encode(FORMAT))
                CLIENT.recv(1024).decode(FORMAT)

                check = CLIENT.recv(1024).decode(FORMAT)
                if check == valUser:
                    messagebox.showwarning("Warning!!!", "Username is already exist!")
                    return
                elif check == Okay:
                    messagebox.showinfo("Notification!", "Welcome, bro!")
                    username.set("")
                    password.set("")
                    confirm_password.set("")
                    return   

                CLIENT.settimeout(5)                            # Chờ phản hồi trong 5s, nếu ko phản hồi thì hiện thông báo dưới
     
            except:     #Không nhận lại phản hồi từ Server
                messagebox.showwarning("Warning!!!", "Server corrupted!")
                # Quay lại GUI nhập IP 
                self.controller.showFrame("HomePage")

app = AppClient()

def Close():
    if app.isClientClose == 0:
        app.End()

app.protocol("WM_DELETE_WINDOW", Close)
app.mainloop()
