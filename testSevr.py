import json
import socket
import threading
HOST = "127.0.0.1"
SERVER_PORT = 63000
FORMAT = "utf8"

LIST = 'list'
LOGIN = 'login'
FAIL = 'fail'
SUCCESS = 'Successfull'
SIGNUP = 'signup'
INVALID = 'invalid'
FORMATPASS = 'wrong format pass'
FORMATUSERNAME = 'wrong format username'
FORMATBANKCODE = 'wrong format bankcode'
DUPLICATEUSER = 'duplicate user name'
with open("accounts.json","r") as f:
    accounts = json.load(f)
with open("hotel.json","r") as f:
    hotel = json.load(f)
def Check_Username(username):
    Alphabet = "abcdefghijklmnopqrstuvwxyz"
    Digit = "0123456789"
    if (len(username) < 5):
        return False
    for i in username:
        if ((i not in Alphabet) and (i not in Digit)):
            return False
    return True
def Check_BankCode(BankCode):
    Digit = "0123456789"
    if (len(BankCode) != 10):
        return False
    for i in BankCode:
        if (i not in Digit):
            return False
    return True
def Check_Password(password):
    if(len(password) < 3):
        return False
    return True
def sendList(conn,list):
    for item in list:
        conn.sendall(item.encode(FORMAT))
        conn.recv(1024)
    msg = "end"
    conn.sendall(msg.encode(FORMAT))
def handleLogin(msg,conn):
    while(msg != INVALID and msg != SUCCESS):
        username = conn.recv(1024).decode(FORMAT)
        conn.sendall(username.encode(FORMAT))
        password = conn.recv(1024).decode(FORMAT)
        conn.sendall(password.encode(FORMAT))
        for cont in accounts:
            if cont['username'] == username and cont['password'] == password :
                msg = SUCCESS
                break
        if(msg != SUCCESS):
            msg = INVALID
        # else:
        #     list = []
        #     for hot in hotel:
        #         string_name = json.dumps(hot['name'],indent=2)
        #         list.append(string_name)
        #     sendList(conn,list)
    conn.sendall(msg.encode(FORMAT))
    if(msg == SUCCESS):
        list = []
        for hot in hotel:
            string_name = hot['name']
            list.append(string_name)
        sendList(conn,list)
def handleSignup(msg,msg2,msg3,msg4,checksignup,conn):
    while(msg != SUCCESS and msg != FORMATUSERNAME and msg2 != FORMATPASS and msg3 != DUPLICATEUSER and msg4 != FORMATBANKCODE):
        username = conn.recv(1024).decode(FORMAT)
        conn.sendall(username.encode(FORMAT))
        password = conn.recv(1024).decode(FORMAT)
        conn.sendall(password.encode(FORMAT))
        BankCode = conn.recv(1024).decode(FORMAT)
        conn.sendall(BankCode.encode(FORMAT))
        checkDuplicate = True
        for cont in accounts:
            if cont['username'] == username :
                msg3 = DUPLICATEUSER
                checkDuplicate = False
                break
        checkBankcode = Check_BankCode(BankCode)
        checkusername = Check_Username(username)
        checkpass = Check_Password(password)
        if(checkusername and checkpass and checkDuplicate and checkBankcode):
            account = {"username": username, "password" : password,"bankcode": BankCode,"Booked room": []}
            accounts.append(account)
            with open("accounts.json","w") as f:
                json.dump(accounts,f,indent=2)
            msg = SUCCESS
        else:
            checksignup = False
            if(checkusername == False):
                msg = FORMATUSERNAME
            if(checkpass == False):
                msg2 = FORMATPASS
            if(checkBankcode == False):
                msg4 = FORMATBANKCODE
    conn.sendall(msg.encode(FORMAT))
    if checksignup == False :
        conn.recv(1024)
        if(msg2 == None):msg2 = 'a'
        if(msg3 == None):msg3 = 'a'
        if(msg4 == None):msg4 = 'a'
        conn.sendall(msg2.encode(FORMAT))
        conn.recv(1024)
        conn.sendall(msg3.encode(FORMAT))
        conn.recv(1024)
        conn.sendall(msg4.encode(FORMAT))
        conn.recv(1024)
def handleClient(conn, addr):
    msg = None
    msg2 = None
    msg3 = None
    while(True):
        try:
            msg = conn.recv(1024).decode(FORMAT)
        except:
            break
        checksignup = True
        msg2 = None
        msg3 = None
        msg4 = None
        if(msg == LOGIN):
            handleLogin(msg,conn)
        elif(msg == SIGNUP):
            handleSignup(msg,msg2,msg3,msg4,checksignup,conn)
        # conn.sendall(msg.encode(FORMAT))
        # if checksignup == False :
        #     conn.recv(1024)
        #     if(msg2 == None):msg2 = 'a'
        #     if(msg3 == None):msg3 = 'a'
        #     if(msg4 == None):msg4 = 'a'
        #     conn.sendall(msg2.encode(FORMAT))
        #     conn.recv(1024)
        #     conn.sendall(msg3.encode(FORMAT))
        #     conn.recv(1024)
        #     conn.sendall(msg4.encode(FORMAT))
        #     conn.recv(1024)

    print("client address:",addr,"finished")
    conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST,SERVER_PORT))
s.listen()
print("SERVER SIDE")
print("server: ", HOST, SERVER_PORT)
print("Waiting for Client")
nClient = 0
while (nClient < 3):
    nClient += 1   
    try:
        conn, addr = s.accept()
        print("client address:",addr)
        print("conn:",conn.getsockname())
        # list = []
        # for hot in hotel:
        #     string_name = hot['name']
        #     list.append(string_name)
        # sendList(conn,list)
        tr = threading.Thread(target = handleClient,args=(conn,addr))
        tr.daemon = True
        tr.start()
    except:
        print("error")
s.close()