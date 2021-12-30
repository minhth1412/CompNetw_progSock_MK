import tkinter as tk                # python 3
from tkinter import ttk
from tkinter.constants import CENTER
from tkinter.messagebox import showinfo
from tkinter import font as tkfont
from GetAPI import *
import json

# cursor chứa dữ liệu của giá trị đồng tiền, lấy từ file webData
try:
    with open("webData.json",'r') as file:
        cursor = json.load(file)
except:
    cursor = getAPIfromWeb()

class SearchingApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Tạo WINDOW cho APP 
        self.title_font = tkfont.Font(family = 'Helvetica', size = 32, weight = "bold", slant = "italic")
        self.title("SEARCHING APP")
        sizex = 845
        sizey = 550
        posx  = 100
        posy  = 100
        self.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
        self.resizable(width = False, height = False)

        # container chứa 3 frame của APP: 1. SearchingPage, 2. SearchingDay, 3. SearchingCurrency
        container = tk.Frame(self)
        container.pack(side = "top")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # Tạo frames cho container
        self.frames = {}
        for F in (SearchingPage, SearchingDay, SearchingCurrency):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame

            # Đặt tất cả các frame page ở cùng một vị trí trên Window của APP
            frame.grid(row = 0, column = 0, sticky = "nsew")

        # Hiện SearchingPage trước tiên
        self.showFrame("SearchingPage")
    
    # Hàm showFrame để hiện các frame page đã lưu trong self.frames
    def showFrame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def Back(self):
        self.destroy()

# Page tra cứu
class SearchingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Là một frame WINDOW của APP nên gọi lại controller (self = tk.Tk)
        label = tk.Label(self, text = "SEARCHING PAGE", font = controller.title_font)
        label.pack(side = "top", pady = 100)

        title_font = tkfont.Font(family = 'Helvetica', size = 14, weight = "bold", slant = "italic")

        DayButton = tk.Button(self, text = " NOW A DAY ", padx = 100, pady = 35, font = title_font,
                            command = lambda: controller.showFrame("SearchingDay"))
        CurrencyButton = tk.Button(self, text = "BY CURRENCY", padx = 91, pady = 35, font = title_font,
                            command = lambda: controller.showFrame("SearchingCurrency"))
        BackButton = tk.Button(self, text = "BACK", padx = 120, pady = 35, font = title_font,
                            command = lambda: controller.Back())
        DayButton.pack()
        CurrencyButton.pack()
        BackButton.pack()
    
class SearchingDay(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.table = self.createTable()

    def createTable(self):
        # Tạo column cho table
        columns = ("currency", "buy_cash", "buy_transfer", "sell")

        # Tạo table
        table = ttk.Treeview(self, columns = columns, show = 'headings')

        # Tạo heading cho bảng tra cứu (table)
        table.heading('currency', text = 'Currency', anchor = CENTER)
        table.heading('buy_cash', text = 'Buy Cash', anchor = CENTER)
        table.heading('buy_transfer', text = 'Buy Transfer', anchor = CENTER)
        table.heading('sell', text = 'Sell', anchor = CENTER)

        # Tạo mảng chuỗi dữ liệu chứa nội dung cần hiện trong bảng 
        items = []
        for n in cursor['results']:
            # Thêm phần chuỗi dữ liệu {currency, buy_cash, buy_transfer, sell} vào items
            items.append((n['currency'], n['buy_cash'], n['buy_transfer'], n['sell']))

        # Thêm phần nội dung vào bảng 
        for contact in items:
            table.insert('', tk.END, values = contact)

        # Tạo bảng table và grid vào frame
        table.bind('<<TreeviewSelect>>', self.selectItem)
        table.grid(row = 0, column = 0, sticky = 'nsew')

        # Tạo thanh cuộn dọc cho table (trục y, góc phải ngoài cùng)
        scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = table.yview)
        table.configure(yscroll = scrollbar.set)
        scrollbar.grid(row = 0, column = 1, sticky = 'ns')

        # Phong chữ
        title_font = tkfont.Font(family = 'Helvetica', size = 14, weight = "bold", slant = "italic")

        # Nút quay về Searching Page
        button = tk.Button(self, text = "Back to Searching Page", font = title_font,
                           command = lambda: self.controller.showFrame("SearchingPage"))
        button.grid(padx = 0, pady = 0, ipadx = 20, ipady = 10)

        return table

    def selectItem(self, event):
        for selectItem in self.table.selection():
            # select item trong chuỗi item đã lưu # show thông tin item vào table
            item = self.table.item(selectItem)
            record = item['values']
            # show thông tin item vào table
            showinfo(title = 'Information', message=','.join(record))

# Callback để chờ lệnh từ button khi search theo currency 
class Callback:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
    def __call__(self):
        self.func(*self.args, **self.kwargs)

# Search theo đồng tiền
class SearchingCurrency(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.items = []
        self.Currency = self.search()

    def search(self):
        # Vẽ frame chứa các button 
        mycanvas = tk.Canvas(self, height = 360, width = 300)
        mycanvas.grid(row = 0,column = 0)

        # Tạo thanh cuộn cho frame chứa button
        yscrollbar = ttk.Scrollbar(self, orient = "vertical", command = mycanvas.yview)
        yscrollbar.grid(row = 0, column = 0, sticky = "ne", rowspan = 100, ipady = 160)

        mycanvas.configure(yscrollcommand = yscrollbar.set)
        mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion = mycanvas.bbox('all')))

        myframe = tk.Frame(mycanvas)
        mycanvas.create_window((0,0), window = myframe, anchor = "nw")

        # Tạo dãy button currency
        result = []
        i = 0
        for p in cursor['results']:  
            # Đọc dữ liệu currency từ cursor
            result.append(p['currency']) 
            currency = tk.Button(myframe, text = p['currency'], width = 40, height = 2, command = Callback(self.showCurrency, p['currency']))
            currency.grid(row = i, column = 0)
            i = i + 1

        # Button back về Searching Page 
        button = tk.Button(self, text = "Back to Searching Page", command = lambda: self.controller.showFrame("SearchingPage"),
                                     height = 2, width = 40)
        button.grid(row = 1, column = 0)  
        
    # Hàm show Currency khi click vào button có mang tiền tệ
    def showCurrency(self, t):
        # Tạo column cho table
        columns = ("currency", "buy_cash", "buy_transfer", "sell")

        # Tạo table
        table = ttk.Treeview(self, columns = columns, show = 'headings', height = 17)
        
        # Định dạng kích thước mỗi cột cho table
        table.column('currency', width = 100)
        table.column('buy_cash', width =  100)
        table.column('buy_transfer', width = 100)
        table.column('sell', width = 100)

        # Tạo heading cho bảng tra cứu (table)
        table.heading('currency', text = 'Currency', anchor = CENTER)
        table.heading('buy_cash', text = 'Buy Cash', anchor = CENTER)
        table.heading('buy_transfer', text = 'Buy Transfer', anchor = CENTER)
        table.heading('sell', text = 'Sell', anchor = CENTER)

        # Tìm phần tử tra cứu trong cursor
        inform = '{}'.format(t)
        for n in cursor['results']:
            if (n['currency'] == inform):
                # Thêm phần chuỗi dữ liệu {currency, buy_cash, buy_transfer, sell} vào items
                self.items.append((n['currency'], n['buy_cash'], n['buy_transfer'], n['sell']))

        # Thêm phần nội dung vào table
        for item in self.items:
            table.insert('', tk.END, values = item)

        # Tạo table và grid vào frame
        table.bind('<<TreeviewSelect>>', self.item_selected)
        table.grid(row= 0, column= 1, sticky= "nw")

        # Cập nhật cho frame
        self.table = table

        # Tạo và grid thanh cuộn cho table
        scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = table.yview)
        table.configure(yscroll = scrollbar.set)
        scrollbar.grid(row = 0, column = 2, sticky = "ns")

    def item_selected(self, event):
        for selected_item in self.table.selection():
            # select item trong chuỗi item đã lưu 
            item = self.table.item(selected_item)
            record = item['values']
            # show thông tin item vào table
            showinfo(title = 'Information', message = ','.join(record))    
