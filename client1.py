import tkinter as tk
import socket

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
class SignUpPage(tk.Frame):
    def __init__(self,parent,appController,client):
        tk.Frame.__init__(self,parent)
        self.label_title = tk.Label(self, text = 'Sign up')
        self.label_notice = tk.Label(self,text='')
        self.label_username = tk.Label(self, text = 'username')
        self.entry_username = tk.Entry(self,bg='light yellow',width=30)
        self.label_noticeUsername = tk.Label(self,text='')
        self.label_password = tk.Label(self, text = 'password')
        self.entry_password = tk.Entry(self,bg='light yellow',width=30)
        self.label_noticePassword = tk.Label(self,text='')
        self.label_RetypePassword = tk.Label(self, text = 'retype password')
        self.entry_RetypePassword = tk.Entry(self,bg='light yellow',width=30)
        self.btn_signup = tk.Button(self,text='Sign up',command=lambda: appController.Signup(self,client))
        self.btn_backlogin = tk.Button(self,text='login ->',command=lambda: appController.showPage(StartPage))
        self.label_title.pack()
        self.label_username.pack()
        self.entry_username.pack()
        self.label_noticeUsername.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.label_noticePassword.pack()
        self.label_RetypePassword.pack()
        self.entry_RetypePassword.pack()
        self.label_notice.pack()
        self.btn_signup.pack()
        self.btn_backlogin.pack()
class HomePage(tk.Frame):
    def __init__(self,parent,appController,client):
        tk.Frame.__init__(self,parent)
        label_login = tk.Label(self,text="You have logging successfully")
        label_title = tk.Label(self, text = 'HOME PAGE')
        hotel_info = tk.Button(self,text='Find hotel information')
        hotel_book = tk.Button(self,text='Book a room in specific hotel')
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
        self.entry_password = tk.Entry(self,bg='light yellow',width=30)
        self.btn_login = tk.Button(self,text='Login',command=lambda: appController.Login(self,client))
        self.btn_signup = tk.Button(self,text='Sign up',command=lambda: appController.showPage(SignUpPage))
        self.label_title.pack()
        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.label_notice.pack()
        self.btn_login.pack()
        self.btn_signup.pack()


class App(tk.Tk):
    def __init__(self,client):
        tk.Tk.__init__(self)
        self.title("My app")
        self.geometry("500x250")
        self.resizable(width=False, height=False)

        container = tk.Frame()

        container.pack(side="top",fill="both",expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}
        for F in (StartPage,HomePage,SignUpPage):
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
                self.showPage(HomePage)
            else:
                curFrame.label_notice["text"] = INVALID
    def Signup(self,curFrame,client):
        username = curFrame.entry_username.get()
        password = curFrame.entry_password.get()
        RetypePassword = curFrame.entry_RetypePassword.get()
        if (RetypePassword != password):
            curFrame.label_notice["text"] = 'Password are not the same'
            return
        else:
            msg = SIGNUP
            client.sendall(msg.encode(FORMAT))
            client.sendall(username.encode(FORMAT))
            client.recv(1024)
            client.sendall(password.encode(FORMAT))
            client.recv(1024)
            msg = client.recv(1024).decode(FORMAT)
            if msg == SUCCESS:
                curFrame.label_noticeUsername["text"] = ''
                curFrame.label_noticePassword["text"] = ''
                curFrame.label_notice["text"] = 'Sign up successfully !'
            else:
                client.sendall(msg.encode(FORMAT))
                msg2 = client.recv(1024).decode(FORMAT)
                client.sendall(msg2.encode(FORMAT))
                if(msg == FORMATUSERNAME):
                    curFrame.label_noticeUsername["text"] = 'Username must have at least 5 character (a-z)(0-9)'
                if(msg2 == FORMATPASS):
                    curFrame.label_noticePassword["text"] = 'Password must have at least 3 character'
    def showPage(self,frameName):
        self.frames[frameName].tkraise()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")
try:
    client.connect((HOST, SERVER_PORT))
except:
    print("error")
app = App(client)
app.mainloop()