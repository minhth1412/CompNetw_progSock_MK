import sys
import socket
import tkinter as tk                # python 3
from tkinter import font as tkfont
from GetAPI import *
import SearchingPage

PORT = 7654
FORMAT = "utf8"
HEADER = 64
try:
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("FAILED TO CREATE CLIENT !!")
    sys.exit();

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

class AppClient(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Tạo WINDOW cho AppClient
        self.title("CLIENT")
        sizex = 845
        sizey = 400
        posx  = 100
        posy  = 100
        self.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
        self.resizable(width = False, height = False)

        # container chứa 3 frame của AppClient: 1. StartPage, 2. SignIn, 3. SignUp
        container = tk.Frame(self)
        container.pack(side = "top")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # Tạo frames cho container
        self.frames = {}
        for F in (StartPage, SignIn, SignUp):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame

            # Đặt tất cả các frame page ở cùng một vị trí trên Window của AppClient
            frame.grid(row = 0, column = 0, sticky = "nsew")

        # Hiện SearchingPage trước tiên
        self.title_font = tkfont.Font(family = 'Helvetica', size = 32, weight = "bold", slant = "italic")
        self.miniFont = tkfont.Font(family = 'Helvetica', size = 14, slant = "italic")
        label = tk.Label(self, text = "CLIENT", font =  self.title_font)     
        ipLabel = tk.Label(self, text = "IP Server: ", font = self.miniFont)
        IP = tk.StringVar()
        ipEntry = tk.Entry(self, textvariable = IP, font = self.miniFont)
        notifyLabel = tk.Label(self, text = "")
        connect = tk.Button(self, text = "CONNECT", padx = 50, pady= 10, font= self.miniFont, command = lambda: self.checkIP(IP))

        label.grid()
        ipLabel.grid()
        ipEntry.grid()
        notifyLabel.grid()
        connect.grid()
    
    def checkIP(self, ip):
        IPServer = str(ip.get())
        HOST = IPServer
        # Đồng nhất port với bên server
        
        SERVER_addr = (HOST, PORT)
        
        notice = ""
        
        try: 
            self.CLIENT.connect(SERVER_addr)       # Kết nối tới SERVER
            self.showFrame("StartPage")
            msg = None
            while (msg != "END"):
                msg = input("Talk to server: ")
                CLIENT.sendall(msg.encode(FORMAT))
                #receive = CLIENT.recv(1024).decode(FORMAT)
                #print("Server respone: ", receive)
                #if (receive == "END"):
                #    msg = receive
        except:
            notice = "SERVER ISN'T RESPONDING!"
            tk.Label(self, text = notice, font = self.miniFont).grid(row = 5)
            CLIENT.close()
        finally:
            notice = "                         "
            tk.Label(self, text = notice, font = self.miniFont).grid(row = 5)
            CLIENT.close()

    # Hàm showFrame để hiện các frame page đã lưu trong self.frames
    def showFrame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def End(self):
        self.destroy()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Là một frame WINDOW của APP nên gọi lại controller (self = tk.Tk)
        self.controller = controller
        label = tk.Label(self, text = "CLIENT", font = controller.title_font)
        label.pack(side = "top", pady = 20)

        self.title_font = tkfont.Font(family = 'Helvetica', size = 14, weight = "bold", slant = "italic")
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
        self.title_font = tkfont.Font(family = 'Helvetica', size = 14, slant = "italic")
        usernameLabel = tk.Label(self, text ="Username: ", font = self.title_font)
        username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable = username, font = self.title_font)

        ##passWord Label
        passwordLabel = tk.Label(self, text = "Password", font = self.title_font )
        password = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable = password, show = '*', font = self.title_font)

        # Chạy hàm checkLogin và nếu success thì import và vào Searching không thì sẽ báo lỗi
        notifyLabel = tk.Label(self, text = "")
        SignInButton = tk.Button(self, text = "Sign In", padx = 30, pady= 5, command = lambda: self.checkAccount(username, password))
        backButton = tk.Button(self, text = "BACK", padx = 35, pady= 5, command = lambda: controller.showFrame("StartPage"))
        
        loginText_label.grid()
        usernameLabel.grid()
        usernameEntry.grid()
        passwordLabel.grid()
        passwordEntry.grid()
        notifyLabel.grid()
        SignInButton.grid()
        backButton.grid()

    def checkAccount(self, Username, Password):
        username = str(Username.get())
        password = str(Password.get())
        notifyFont = tkfont.Font(family = 'Helvetica', size = 10, slant = "italic")
        notify = ""
        CLIENT.sendall(username.encode(FORMAT))
        # lệnh client.recv() để client gửi tuần tự username - pass về cho server
        checkingUser = CLIENT.recv(1024)
        if (checkingUser != 'INVALID ACCOUNT'):
            CLIENT.sendall(password.encode(FORMAT))
            # CLient nhận phản hồi từ server tài khoản có đúng hay không
            check = CLIENT.recv(1024)
            if (check == 'FALSE'):
                print('PASSWORD OR USERNAME IS INCORRECT')
        
        #check = 0
        if (username == '' or password == ''):
            notify = "Please entering username or password"
            pad = 0            
        elif (username != "asd" or password != "asd"):
            notify = "Username or password is wrong"
            pad = 30
        else:
            notify = "Sign in successfull"
            pad = 50
            check = 1        

        Username.set("")
        Password.set("")
        notifyLabel = tk.Label(self, text = notify, font = notifyFont, padx = pad)
        notifyLabel.grid(row = 5)
        if (check == 1):
            app = SearchingPage.SearchingApp()
            app.mainloop()

class SignUp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.controller = controller

        loginText_label = tk.Label(self, text = "SIGN UP CLIENT", font = self.controller.title_font)      
        self.title_font = tkfont.Font(family = 'Helvetica', size = 14, slant = "italic")

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

        # Chạy hàm checkLogin và nếu success thì import và vào Searching không thì sẽ báo lỗi
        notifyLabel = tk.Label(self, text = "")  
        loginButton = tk.Button(self, text = "Sign Up", padx = 30, pady= 5, command = lambda: self.checkPassWord(confirm_password, password) )            
        backButton = tk.Button(self, text = "BACK", padx = 35, pady= 5, command = lambda: controller.showFrame("StartPage"))
        
        loginText_label.grid()
        usernameLabel.grid()
        usernameEntry.grid()
        passwordLabel.grid()
        passwordEntry.grid()
        confirm_passwordLabel.grid()
        confirm_passwordEntry.grid()
        notifyLabel.grid()
        loginButton.grid()
        backButton.grid()
        
    def checkPassWord(self, confirm_password, password):
        confirmPassword = str(confirm_password.get())
        Password = str(password.get())
        notify = ""   
        if (confirmPassword == '' or Password == ''):
            notify = "Please entering password or confirm password"        
        elif (confirmPassword == Password):
            notify = "Creating account successfully !!"
        else:
            notify = "Confirm password is wrong !!"
        
        notifyFont = tkfont.Font(family = 'Helvetica', size = 10, slant = "italic")
        notifyLabel = tk.Label(self, text = notify, font = notifyFont)
        notifyLabel.grid(row = 7)

if __name__ == "__main__":
    app = AppClient()
    app.mainloop()