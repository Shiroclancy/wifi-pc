import tkinter as tk
import socket
import json
from tkinter.constants import END, SINGLE

HOST = "127.0.0.1"
SERVER_PORT = 63000
FORMAT = "utf8"

LIST = "list"
LOGIN = "login"
FAIL = 'fail'
SUCCESS = 'Successfull'
SIGNUP = 'signup'
INVALID = 'invalid'
FORMATPASS = 'wrong format pass'
FORMATUSERNAME = 'wrong format username'
FORMATBANKCODE = 'wrong format bankcode'
DUPLICATEUSER = 'duplicate user name'
listtHotel = []
acc = {}
def recvListt(client):
    list = []
    item = client.recv(1024).decode(FORMAT)
    while(item != "end"):
        list.append(item)
        client.sendall(item.encode(FORMAT))
        item = client.recv(1024).decode(FORMAT)
    return list

def inputhotel(hotellist):
    for i in listtHotel:
        hotellist.insert(END, "hotel " + i)

class BookingPage(tk.Frame):
    def __init__(self,parent,app,client):
        tk.Frame.__init__(self,parent)
        title = tk.Label(self,text=" Book a hotel room")
        hotelName = tk.Label(self,text="Hotel name/code: ")
        roomtype = tk.Label(self,text="Room type: ")
        DateOfEntry = tk.Label(self, text = 'Date of entry: ')
        DateOfExit = tk.Label(self,text="Date of exit: ")
        Home= tk.Button(self,text="Back to \n home page",command=lambda: app.showPage(HomePage))
        Enter= tk.Button(self,text="Enter")
        Note = tk.Label(self,text="Note: ")
        name = tk.Entry(self,bg='white',width=30)
        entry = tk.Entry(self,bg='white',width=30)
        exit = tk.Entry(self,bg='white',width=30)
        room = tk.Entry(self,bg='white',width=30)
        Enote = tk.Entry(self,bg='white',width=30)

        self.grid_rowconfigure(1,weight =1)
        self.grid_rowconfigure(13,weight =1)
        self.grid_columnconfigure(0,weight =1)
        self.grid_columnconfigure(3,weight =1)

        title.grid(row=0,column=1,columnspan=2)

        hotelName.grid(row=2,column=1,sticky="w")
        name.grid(row=2,column=2)
        self.grid_rowconfigure(3,minsize=10)

        roomtype.grid(row=4,column=1,sticky="w")
        room.grid(row=4,column=2)
        self.grid_rowconfigure(5,minsize=10)

        DateOfEntry.grid(row=6,column=1,sticky="w")
        entry.grid(row=6,column=2)
        self.grid_rowconfigure(7,minsize=10)

        DateOfExit.grid(row=8,column=1,sticky="w")
        exit.grid(row=8,column=2)
        self.grid_rowconfigure(9,minsize=10)

        Note.grid(row=10,column=1,sticky="w")
        Enote.grid(row=10,column=2)
        self.grid_rowconfigure(11,minsize=20)

        Home.grid(row=12,column=1,sticky="w")
        Enter.grid(row=12,column=2,sticky="e")
    
class HotelInfoPage(tk.Frame):
    def __init__(self,parent,app,client):
        tk.Frame.__init__(self,parent)
        title = tk.Label(self,text="Finding hotel avaiable room")
        app.hotellist= tk.Listbox(self,bg='white',selectmode=SINGLE,height =15)
        DateOfEntry = tk.Label(self, text = 'Date of entry: ')
        DateOfExit = tk.Label(self,text="Date of exit: ")
        scrollbar = tk.Scrollbar(app.hotellist,)
        slash = tk.Label(self,text="/")
        slash1 = tk.Label(self,text="/")
        slash2 = tk.Label(self,text="/")
        slash3 = tk.Label(self,text="/")

        dayentry = tk.Entry(self,bg = 'white',width=2)
        monthentry = tk.Entry(self,bg = 'white',width=2)
        yearentry = tk.Entry(self,bg = 'white',width=4)

        dayexit = tk.Entry(self,bg = 'white',width=2)
        monthexit = tk.Entry(self,bg = 'white',width=2)
        yearexit = tk.Entry(self,bg = 'white',width=4)
        # listt = recvListt(client)
        

        Home= tk.Button(self,text="Back to \n home page",command=lambda: (app.showPage(HomePage),app.hotellist.delete(0,END)))
        Enter= tk.Button(self,text="Enter")
        
        title.grid(row=0,column=0,columnspan=10,sticky="we")
        self.grid_rowconfigure(1,minsize=10)
        self.grid_columnconfigure(0,minsize=10)
              
        app.hotellist.grid(row=2,column=1,rowspan = 5)
        # scrollbar.grid(row=2,column=1,rowspan = 5,sticky='ens')
        self.grid_columnconfigure(2, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        DateOfEntry.grid(row=3,column=3)
        DateOfExit.grid(row=4,column=3)

        dayentry.grid(row=3,column=4)
        dayexit.grid(row=4,column=4)
        slash.grid(row=3,column=5)
        slash1.grid(row=4,column=5)
                
        monthentry.grid(row=3,column=6)
        monthexit.grid(row=4,column=6)
        slash2.grid(row=3 ,column=7)
        slash3.grid(row=4,column=7)

        yearentry.grid(row=3,column=8)
        yearexit.grid(row=4,column=8)

        self.grid_columnconfigure(9, weight = 1)
        self.grid_rowconfigure(6, weight = 1)
        

        Home.grid(row=6,column=3)
        Enter.grid(row=6,column=8)
        self.grid_rowconfigure(7, weight = 1)
       
class SignUpPage(tk.Frame):
    def __init__(self,parent,appController,client):
        tk.Frame.__init__(self,parent)
        self.label_title = tk.Label(self, text = 'Sign up')
        self.label_notice = tk.Label(self,text='')
        self.label_username = tk.Label(self, text = 'Username: ')
        self.entry_username = tk.Entry(self,bg='light yellow',width=30)
        self.label_noticeUsername = tk.Label(self,text='')
        self.label_password = tk.Label(self, text = 'Password: ')
        self.entry_password = tk.Entry(self,bg='light yellow',width=30)
        self.label_noticePassword = tk.Label(self,text='')
        self.label_RetypePassword = tk.Label(self, text = 'Confirm password: ')
        self.entry_RetypePassword = tk.Entry(self,bg='light yellow',width=30)
        self.label_noticeRetypePassword = tk.Label(self,text='')
        self.label_BankCode = tk.Label(self, text = 'Bank Code: ')
        self.entry_BankCode = tk.Entry(self,bg='light yellow',width=30)
        self.btn_signup = tk.Button(self,text='Sign up',command=lambda: appController.Signup(self,client))
        self.btn_backlogin = tk.Button(self,text='Back to/nlogin',command=lambda: appController.showPage(StartPage))

        self.grid_rowconfigure(1,weight =1)
        self.grid_rowconfigure(16,weight =1)
        self.grid_columnconfigure(0,weight =1)
        self.grid_columnconfigure(3,weight =1)

        self.label_title.grid(row=0,column=1,columnspan=2)       
        
        self.label_username.grid(row=3,column=1,sticky="w")
        self.entry_username.grid(row=3,column=2,padx=10)
        self.label_noticeUsername.grid(row=4,column=1,columnspan=2)
        
        self.label_password.grid(row=6,column=1,sticky="w")
        self.entry_password.grid(row=6,column=2,padx=10)
        self.label_noticePassword.grid(row=7,column=1,columnspan=2)

        self.label_RetypePassword.grid(row=9,column=1,sticky="w")
        self.entry_RetypePassword.grid(row=9,column=2,padx=10)
        self.label_noticeRetypePassword.grid(row=10,column=1,columnspan=2)

        self.label_BankCode.grid(row=12,column=1,sticky="w")
        self.entry_BankCode.grid(row=12,column=2,padx=10)
        self.label_notice.grid(row=13,column=1,columnspan=2)
        self.grid_rowconfigure(14,minsize=10)

        self.btn_backlogin.grid(row=15,column=1,sticky="w")
        self.btn_signup.grid(row=15,column=2,sticky="e")

class HomePage(tk.Frame):
    def __init__(self,parent,appController,client):
        tk.Frame.__init__(self,parent)
        label_login = tk.Label(self,text="You have logging successfully")
        label_title = tk.Label(self, text = 'HOME PAGE')
        hotel_info = tk.Button(self,text='Find hotel information',command=lambda:(appController.showPage(HotelInfoPage), inputhotel(appController.hotellist)))
        hotel_book = tk.Button(self,text='Book a room in specific hotel',command=lambda:appController.showPage(BookingPage))
        hotel_removebooking = tk.Button(self,text='logout')
        blank=tk.Label(self,text="")
        btn_logout = tk.Button(self,text='logout',command=lambda:appController.showPage(StartPage))
        label_title.pack()
        label_login.pack()
        hotel_info.pack(pady=10)
        hotel_book.pack(pady=10)
        btn_logout.pack(pady=10)

class StartPage(tk.Frame):
    def __init__(self,parent,appController,client):
        tk.Frame.__init__(self,parent)

        self.label_title = tk.Label(self, text = 'LOGIN')
        self.label_notice = tk.Label(self,text='',bg='bisque')
        self.label_username = tk.Label(self, text = 'username')
        self.entry_username = tk.Entry(self,bg='light yellow',width=30)
        self.label_password = tk.Label(self, text = 'password')
        self.entry_password = tk.Entry(self,bg='light yellow',width=30,show="*")
        self.btn_login = tk.Button(self,text='Login',command=lambda: appController.Login(self,client))
        self.btn_signup = tk.Button(self,text='Sign up',command=lambda: appController.showPage(SignUpPage))
        
        self.grid_rowconfigure(3,weight =1)
        self.grid_rowconfigure(9,weight =1)
        self.grid_columnconfigure(0,weight =1)
        self.grid_columnconfigure(3,weight =1)

        self.label_title.grid(row=0,column=1,columnspan=2)
        self.label_notice.grid(row=1,column=1,columnspan=2)

        self.label_username.grid(row=4,column=1)
        self.entry_username.grid(row=4,column=2,padx=10)
        self.grid_rowconfigure(5,minsize=20)
        
        self.label_password.grid(row=6,column=1)
        self.entry_password.grid(row=6,column=2,padx=10)
        self.grid_rowconfigure(7,minsize=30)

        self.btn_signup.grid(row=8,column=1,sticky='w')
        self.btn_login.grid(row=8,column=2,sticky='e')

class App(tk.Tk):
    def __init__(self,client):
        tk.Tk.__init__(self)
        self.title("My app")
        self.geometry("500x300")
        self.resizable(width=False, height=False)

        container = tk.Frame()

        container.pack(side="top",fill="both",expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}
        for F in (StartPage,HomePage,SignUpPage,HotelInfoPage,BookingPage):
            frame = F(container,self,client)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
        self.frames[StartPage].tkraise()
    def Login(self,curFrame,client):
        username = curFrame.entry_username.get()
        password = curFrame.entry_password.get()
        print(username,password)

        if (username == '' or password == ''):
            curFrame.label_notice["text"] = 'failed login'
            return
        else:
            msg = LOGIN
            client.sendall(msg.encode(FORMAT))
            client.sendall(username.encode(FORMAT))
            client.recv(1024)
            client.sendall(password.encode(FORMAT))
            client.recv(1024)
            msg = client.recv(1024).decode(FORMAT)
            if msg == SUCCESS:
                client.sendall(msg.encode(FORMAT))
                global acc
                temp = client.recv(1024).decode(FORMAT)
                client.sendall(temp.encode(FORMAT))
                acc = json.dumps(temp)
                print(acc)
                global listtHotel
                listtHotel = recvListt(client)
                self.showPage(HomePage)
            else:
                curFrame.label_notice["text"] = INVALID
    def Signup(self,curFrame,client):
        username = curFrame.entry_username.get()
        password = curFrame.entry_password.get()
        BankCode = curFrame.entry_BankCode.get()
        RetypePassword = curFrame.entry_RetypePassword.get()
        if(username == '' or password == '' or RetypePassword == '' or BankCode == ''):
            curFrame.label_noticeUsername["text"] = ''
            curFrame.label_noticePassword["text"] = ''
            curFrame.label_noticeRetypePassword["text"] = ''
            curFrame.label_notice["text"] = 'Fill your information in the blank fields'
            return
        else:
            curFrame.label_notice["text"] = ''
        if (RetypePassword != password):
            curFrame.label_noticeUsername["text"] = ''
            curFrame.label_noticePassword["text"] = ''
            curFrame.label_noticeRetypePassword["text"] = ''
            curFrame.label_noticeRetypePassword["text"] = 'Wrong password'
            return
        else:
            curFrame.label_noticeRetypePassword["text"] = ''
        msg = SIGNUP
        client.sendall(msg.encode(FORMAT))
        client.sendall(username.encode(FORMAT))
        client.recv(1024)
        client.sendall(password.encode(FORMAT))
        client.recv(1024)
        client.sendall(BankCode.encode(FORMAT))
        client.recv(1024)
        msg = client.recv(1024).decode(FORMAT)
        if msg == SUCCESS:
            curFrame.label_noticeUsername["text"] = ''
            curFrame.label_noticePassword["text"] = ''
            curFrame.label_noticeRetypePassword["text"] = ''
            curFrame.label_notice["text"] = 'Sign up successfully !'
        else:
            curFrame.label_notice["text"] = ''
            client.sendall(msg.encode(FORMAT))
            msg2 = client.recv(1024).decode(FORMAT)
            client.sendall(msg2.encode(FORMAT))
            msg3 = client.recv(1024).decode(FORMAT)
            client.sendall(msg3.encode(FORMAT))
            msg4 = client.recv(1024).decode(FORMAT)
            client.sendall(msg4.encode(FORMAT))
            if(msg3 == DUPLICATEUSER):
                curFrame.label_noticeUsername["text"] = 'Already has this username'
            else:
                curFrame.label_noticeUsername["text"] = ''
                if(msg == FORMATUSERNAME):
                    curFrame.label_noticeUsername["text"] = 'Username must have at least 5 character (a-z)(0-9)'
                if(msg2 == FORMATPASS):
                    curFrame.label_noticePassword["text"] = 'Password must have at least 3 character'
                else:
                    curFrame.label_noticePassword["text"] = ''
                if(msg4 == FORMATBANKCODE):
                    curFrame.label_notice["text"] = 'Bank code must have 10 digit'
                else:
                    curFrame.label_notice["text"] = ''
    def showPage(self,frameName):
        self.frames[frameName].tkraise()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")
try:
    client.connect((HOST, SERVER_PORT))
    # listt = recvListt(client)
except:
    print("error")
app = App(client)
app.mainloop()


