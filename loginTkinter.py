import tkinter as tk
class HomePage(tk.Frame):
    def __init__(self,parent,appController):
        tk.Frame.__init__(self,parent)
        label_title = tk.Label(self, text = 'HOME PAGE')
        btn_logout = tk.Button(self,text='logout',command=lambda:appController.showPage(StartPage))
        label_title.pack()
        btn_logout.pack()

class StartPage(tk.Frame):
    def __init__(self,parent,appController):
        tk.Frame.__init__(self,parent)

        self.label_title = tk.Label(self, text = 'LOGIN')
        self.label_notice = tk.Label(self,text='',bg='bisque')
        self.label_username = tk.Label(self, text = 'username')
        self.entry_username = tk.Entry(self,bg='light yellow')
        self.label_password = tk.Label(self, text = 'password')
        self.entry_password = tk.Entry(self,bg='light yellow')
        self.btn_login = tk.Button(self,text='login',command=lambda: appController.Login(self))

        self.label_title.pack()
        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.label_notice.pack()
        self.btn_login.pack()


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("My app")
        self.geometry("500x200")
        self.resizable(width=False, height=False)

        container = tk.Frame()
        container.configure(bg="red")

        container.pack(side="top",fill="both",expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}
        for F in (StartPage,HomePage):
            frame = F(container,self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
        self.frames[StartPage].tkraise()

    def Login(self,curFrame):
        username = curFrame.entry_username.get()
        password = curFrame.entry_password.get()
        print(username,password)

        if (username == '' or password == ''):
            curFrame.label_notice["text"] = 'failed login'
            return

    def showPage(self,frameName):
        self.frames[frameName].tkraise()


app = App()
app.mainloop()