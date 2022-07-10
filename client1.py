import tkinter as tk
import socket
import json
from tkinter.constants import END, SINGLE, TRUE

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
FINDROOM = 'room information'
FINDROOMBOOK = 'room book'
checkboxlist=[]
listtHotelName = []
acc = {}
roomlist=[]
bedlist=[]
roomAvaiInfo = []
roomAvaiBook = []
def sendList(client,list):
    for item in list:
        client.sendall(item.encode(FORMAT))
        client.recv(1024)
    msg = "end"
    client.sendall(msg.encode(FORMAT))

def recvListt(client):
    list = []
    item = client.recv(1024).decode(FORMAT)
    while(item != "end"):
        list.append(item)
        client.sendall(item.encode(FORMAT))
        item = client.recv(1024).decode(FORMAT)
    return list

def inputhotel(hotellist):
    for i in listtHotelName:
        hotellist.insert(END, "hotel " + i)

def inputroom(roomlist):
    for i in range(20):
        roomlist.insert(END, "room " + i)

def clickEventHotellist(event):
    temp = app.hotellist.curselection()
    if temp:
        app.frames[HotelInfoPage].indexHotel = temp[0]

class BookRoom(tk.Frame):
    def __init__(self,parent,app,client):
        tk.Frame.__init__(self,parent)
        title = tk.Label(self,text=" Book hotel room")
        scrollbar = tk.Scrollbar(self,bg='white')

        canvas=tk.Canvas(self,bg='red',yscrollcommand=scrollbar.set)
        app.roomlist= tk.Frame(canvas,bg='white')
        canvas.create_window(1,1,window= app.roomlist)
        app.roomlist.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        roomtype = tk.Label(app.roomlist,text="Room type",bg='white')
        bedtype = tk.Label(app.roomlist,text="Bed type",bg='white')
        Describe = tk.Label(app.roomlist,text="Describe",bg='white')
        Price = tk.Label(app.roomlist,text="Price",bg='white')
        image = tk.Label(app.roomlist,text="Image",bg='white')

        Home= tk.Button(self,text="Go back",command=lambda: app.showPage(HomePage))
        Enter= tk.Button(self,text="Enter",command=lambda: app.showPage(BookRoom))
        title.grid(row=0,column=0,columnspan=10)
        self.grid_columnconfigure(0,minsize=25)

        scrollbar.grid(row=2,column=2,sticky="sn")
        scrollbar.config(command=canvas.yview)

        self.grid_columnconfigure(3,minsize=25)
        self.grid_rowconfigure(1,minsize=25)

        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)
        canvas.grid(row=2,column=1,sticky="wesn")

        roomtype.grid(row=0,column=0,sticky='nwse')
        bedtype.grid(row=0,column=1,sticky='nwse')
        Describe.grid(row=0,column=2,sticky='nwse')
        Price.grid(row=0,column=3,sticky='nwse')
        image.grid(row=0,column=4,sticky='nwse')
        app.roomlist.grid_rowconfigure(1,minsize=20)
        for i in range(5):
            app.roomlist.grid_columnconfigure(i,minsize=146)

        for i in range(len(roomAvaiBook)):
            var=tk.IntVar()
            check= tk.Checkbutton(app.roomlist,text=roomAvaiBook[i]['Room Type'],variable=var,bg='yellow')
            checkboxlist.append(var.get())
            label= tk.Label(app.roomlist,text=roomAvaiBook[i]["Bed Type"],bg='white')
            label1= tk.Label(app.roomlist,text=roomAvaiBook[i]["Describe"],wraplength=150,bg='white')
            label2= tk.Label(app.roomlist,text=roomAvaiBook[i]["Price"],bg='white')
            #label3= tk.Label(app.roomlist,bitmap=roomAvaiBook[i]["Image"])
            check.grid(row=i+2,column=0,sticky='w')
            label.grid(row=i+2,column=1,sticky='w')
            label1.grid(row=i+2,column=2,sticky='w')
            label2.grid(row=i+2,column=3)
            #label3.grid(row=i+2,column=4,sticky='nwse')
        self.grid_rowconfigure(3,minsize=20)

        Home.grid(row=4,column=1,sticky="w")
        Enter.grid(row=4,column=1,sticky="e")

        self.grid_rowconfigure(5,minsize=25) 
      
class BookingPage(tk.Frame):
    def __init__(self,parent,app,client):       
        tk.Frame.__init__(self,parent)
        notice = tk.Label(self,text='',bg='bisque')
        title = tk.Label(self,text=" Book a hotel room")
        hotelName = tk.Label(self,text="Hotel name/code: ")
        roomtype = tk.Label(self,text="Room type: ")
        bedtype = tk.Label(self,text="Bed type: ")
        DateOfEntry = tk.Label(self, text = 'Date of entry: ')
        DateOfExit = tk.Label(self,text="Date of exit: ")
        self.check1 = tk.IntVar()
        self.check2 = tk.IntVar()
        self.check3 = tk.IntVar()
        self.check4 = tk.IntVar()
        self.check5 = tk.IntVar()
        Stand = tk.Checkbutton(self,text="Standard Room",variable=self.check1)
        Super = tk.Checkbutton(self,text="Superior Room",variable=self.check2)
        Single = tk.Checkbutton(self,text="Single Bed",variable=self.check3)
        Twin = tk.Checkbutton(self,text="Twin Bed",variable=self.check4)
        Double = tk.Checkbutton(self,text="Double Bed",variable=self.check5)
        def RoomBedlist():
            roomlist.clear()
            bedlist.clear()
            if(self.check1.get()==1):
                roomlist.append("Standard Room")
            if(self.check2.get()==1):
                roomlist.append("Superior Room")
            if(self.check3.get()==1):
                bedlist.append("Single Bed")
            if(self.check4.get()==1):
                bedlist.append("Twin Bed")
            if(self.check5.get()==1):
                bedlist.append("Double Bed")
            for i in (self.check1,self.check2,self.check3,self.check4,self.check5):
                i.set(0)
            # check list
            #print(roomlist,bedlist)
        Home= tk.Button(self,text="Back to \n home page",command=lambda: app.showPage(HomePage))
        Enter= tk.Button(self,text="Enter",command=lambda: (app.showPage(BookRoom),RoomBedlist(),self.BookedRoomList(client)))
        Note = tk.Label(self,text="Note: ")
        self.name = tk.Entry(self,bg='white',width=30)        
        Enote = tk.Entry(self,bg='white',width=30)
        Date = tk.Frame(self)

        slash = tk.Label(Date,text="/")
        slash1 = tk.Label(Date,text="/")
        slash2 = tk.Label(Date,text="/")
        slash3 = tk.Label(Date,text="/")

        self.dayentry = tk.Entry(Date,bg = 'white',width=2)
        self.monthentry = tk.Entry(Date,bg = 'white',width=2)
        self.yearentry = tk.Entry(Date,bg = 'white',width=4)

        self.dayexit = tk.Entry(Date,bg = 'white',width=2)
        self.monthexit = tk.Entry(Date,bg = 'white',width=2)
        self.yearexit = tk.Entry(Date,bg = 'white',width=4)

        self.grid_rowconfigure(1,weight =1)
        self.grid_rowconfigure(15,weight =1)
        self.grid_columnconfigure(0,weight =1)
        self.grid_columnconfigure(8,weight =1)

        title.grid(row=0,column=0,columnspan=10)
        notice.grid(row=1,column=0,columnspan=10,sticky='n')

        hotelName.grid(row=2,column=1,sticky="w")
        self.name.grid(row=2,column=2,columnspan=5)
        self.grid_rowconfigure(3,minsize=10)

        roomtype.grid(row=4,column=1,sticky="w")
        Stand.grid(row=4,column=2)
        Super.grid(row=4,column=3)
        self.grid_rowconfigure(5,minsize=10)

        bedtype.grid(row=6,column=1,sticky="w")
        Single.grid(row=6,column=2)
        Double.grid(row=6,column=3)
        Twin.grid(row=6,column=4)
        self.grid_rowconfigure(7,minsize=10)
        Date.grid(row=8,column=2,rowspan=3,columnspan=3)

        DateOfEntry.grid(row=8,column=1,sticky="w")
        self.grid_rowconfigure(9,minsize=10)
        DateOfExit.grid(row=10,column=1,sticky="w")
        
        self.dayentry.grid(row=8,column=2)
        self.dayexit.grid(row=10,column=2)
        slash.grid(row=8,column=3)
        slash1.grid(row=10,column=3)
                
        self.monthentry.grid(row=8,column=4)
        self.monthexit.grid(row=10,column=4)
        slash2.grid(row=8,column=5)
        slash3.grid(row=10,column=5)

        self.yearentry.grid(row=8,column=6)
        self.yearexit.grid(row=10,column=6)
        self.grid_rowconfigure(11,minsize=10)

        Note.grid(row=12,column=1,sticky="w")
        Enote.grid(row=12,column=2,columnspan=5)
        self.grid_rowconfigure(13,minsize=20)

        Home.grid(row=14,column=1,sticky="w")
        Enter.grid(row=14,column=7,sticky="e")

    def BookedRoomList(self,client):
        hotelID = self.name.get()
        global roomlist
        global bedlist
        roomtype = roomlist
        bedtype = bedlist
        DateEntry = [self.yearentry.get(),self.monthentry.get(),self.dayentry.get()]
        DateLeaving = [self.yearexit.get(),self.monthexit.get(),self.dayexit.get()]
        msg = FINDROOMBOOK
        client.sendall(msg.encode(FORMAT)) 
        sendList(client,DateEntry)
        client.recv(1024) 
        sendList(client,DateLeaving)
        client.recv(1024)
        client.sendall(hotelID.encode(FORMAT))
        client.recv(1024)
        # client.sendall(roomtype.encode(FORMAT))
        sendList(client,roomtype)
        client.recv(1024)
        sendList(client,bedtype)
        client.recv(1024)
        global roomAvaiBook
        roomAvaiBook = app.frames[HotelInfoPage].recvListroomAvailable(client)
            # roomavai = json.loads(roomavai)
        for rom in roomAvaiBook:        
            print(rom,'\n')
    
class HotelInfoPage(tk.Frame):
    def __init__(self,parent,app,client):
        tk.Frame.__init__(self,parent)
        notice = tk.Label(self,text='Cant leave blank space',bg='bisque')
        title = tk.Label(self,text="Finding hotel avaiable room")
        DateOfEntry = tk.Label(self, text = 'Date of entry: ')
        DateOfExit = tk.Label(self,text="Date of exit: ")
        scrollbar = tk.Scrollbar(self,bg='white')
        app.hotellist= tk.Listbox(self,bg='white',selectmode=SINGLE,height =15,width =30,exportselection=False,yscrollcommand = scrollbar.set)
        slash = tk.Label(self,text="/")
        slash1 = tk.Label(self,text="/")
        slash2 = tk.Label(self,text="/")
        slash3 = tk.Label(self,text="/")

        self.dayentry = tk.Entry(self,bg = 'white',width=2)
        self.monthentry = tk.Entry(self,bg = 'white',width=2)
        self.yearentry = tk.Entry(self,bg = 'white',width=4)

        self.dayexit = tk.Entry(self,bg = 'white',width=2)
        self.monthexit = tk.Entry(self,bg = 'white',width=2)
        self.yearexit = tk.Entry(self,bg = 'white',width=4)
        self.indexHotel = None
        # listt = recvListt(client)
        app.hotellist.bind('<<ListboxSelect>>', clickEventHotellist)

        Home= tk.Button(self,text="Back to \n home page",command=lambda: (app.showPage(HomePage),self.DeleteThing()))
        Enter= tk.Button(self,text="Enter",command=lambda: (app.showPage(BookRoom),self.show()))
        
        title.grid(row=0,column=0,columnspan=10,sticky="we")
        self.grid_rowconfigure(1,minsize=10)
        self.grid_columnconfigure(0,minsize=10)
              
        app.hotellist.grid(row=2,column=1,rowspan = 5)
        scrollbar.grid(row=2,column=2,rowspan = 5,ipady=95)
        self.grid_columnconfigure(3, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        DateOfEntry.grid(row=3,column=4)
        DateOfExit.grid(row=4,column=4)

        self.dayentry.grid(row=3,column=5)
        self.dayexit.grid(row=4,column=5)
        slash.grid(row=3,column=6)
        slash1.grid(row=4,column=6)
                
        self.monthentry.grid(row=3,column=7)
        self.monthexit.grid(row=4,column=7)
        slash2.grid(row=3 ,column=8)
        slash3.grid(row=4,column=8)

        self.yearentry.grid(row=3,column=9)
        self.yearexit.grid(row=4,column=9)
        notice.grid(row=5,column=4,columnspan=6)

        self.grid_columnconfigure(10, weight = 1)
        self.grid_rowconfigure(6, weight = 1)
        

        Home.grid(row=6,column=4)
        Enter.grid(row=6,column=9)
        self.grid_rowconfigure(7, weight = 1)
    def recvListroomAvailable(self,client):
        list = []
        item = client.recv(1024).decode(FORMAT)
        while(item != "end"):
            # item = json.loads(item)
            list.append(json.loads(item))
            client.sendall(item.encode(FORMAT))
            item = client.recv(1024).decode(FORMAT)
        return list
    def DeleteThing(self):
        app.hotellist.delete(0,END)
        app.frames[HotelInfoPage].indexHotel = None
    def InputHotelName(self,hotellist):
        for i in listtHotelName:
            hotellist.insert(END, "hotel " + i)
    def show(self):
        print(app.frames[HotelInfoPage].indexHotel)
        Dayentry =self.dayentry.get()
        Monthentry =self.monthentry.get()
        Yearentry =self.yearentry.get()

        Dayexit =self.dayexit.get()
        Monthexit =self.monthexit.get()
        Yearexit =self.yearexit.get()

        # if(Dayentry == '' or Monthentry == '' or Yearentry == '' or Dayexit == '' or Monthexit == '' or Yearexit == ''):
            # label notice
        # if(app.frames[HotelInfoPage].indiceHotel == None):
            #label notice
        listentry = [Yearentry, Monthentry, Dayentry]
        listexit = [Yearexit, Monthexit, Dayexit]
        msg = FINDROOM
        client.sendall(msg.encode(FORMAT)) 
        sendList(client,listentry)
        client.recv(1024) 
        sendList(client,listexit)
        client.recv(1024)
        client.sendall(str(app.frames[HotelInfoPage].indexHotel).encode(FORMAT))
        client.recv(1024)
        global roomAvaiInfo
        roomAvaiInfo = self.recvListroomAvailable(client)
        # roomavai = json.loads(roomavai)
        for rom in roomAvaiInfo:        
            print(rom,'\n')   

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
        appController.geometry("800x500")
        label_login = tk.Label(self,text="You have logging successfully")
        label_title = tk.Label(self, text = 'HOME PAGE')
        hotel_info = tk.Button(self,text='Find hotel information',command=lambda:(appController.showPage(HotelInfoPage), app.frames[HotelInfoPage].InputHotelName(appController.hotellist)))
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
        for F in (StartPage,HomePage,SignUpPage,HotelInfoPage,BookingPage,BookRoom):
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
                ms = 'ok'
                client.sendall(msg.encode(FORMAT))
                global acc
                temp = client.recv(10000).decode(FORMAT)
                client.sendall(ms.encode(FORMAT))
                acc = json.loads(temp)
                print(acc)
                global listtHotelName
                listtHotelName = recvListt(client)
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


