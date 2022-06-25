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
with open("accounts.json","r") as f:
    content = json.load(f)

def Check_Username(username):
    Alphabet = "abcdefghijklmnopqrstuvwxyz"
    Digit = "0123456789"
    if (len(username) < 5):
        return False
    for i in username:
        if ((i not in Alphabet) and (i not in Digit)):
            return False
    return True

def Check_Password(password):
    if(len(password) < 3):
        return False
    return True

def recvList(conn):
    list = []
    item = conn.recv(1024).decode(FORMAT)
    while(item != "end"):
        list.append(item)
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    return list



def handleClient(conn, addr):
    msg = None
    msg2 = None
    while(True):
        msg = conn.recv(1024).decode(FORMAT)
        checksignup = False
        msg2 = None
        while(msg != INVALID and msg != SUCCESS and msg != FORMATUSERNAME and msg2 != FORMATPASS):
            username = conn.recv(1024).decode(FORMAT)
            conn.sendall(username.encode(FORMAT))
            password = conn.recv(1024).decode(FORMAT)
            conn.sendall(password.encode(FORMAT))
            if(msg == LOGIN):
                for cont in content:
                    if cont['username'] == username and cont['password'] == password :
                        msg = SUCCESS
                        break
                if(msg != SUCCESS):
                    msg = INVALID
                checksignup = True
            if(msg == SIGNUP):
                checkusername = Check_Username(username)
                checkpass = Check_Password(password)
                if(checkusername and checkpass):
                    account = {"username": username, "password" : password}
                    content.append(account)
                    with open("accounts.json","w") as f:
                        json.dump(content,f,indent=2)
                    msg = SUCCESS
                    checksignup = True
                else:
                    if(checkusername == False):
                        msg = FORMATUSERNAME
                    if(checkpass == False):
                        msg2 = FORMATPASS

        conn.sendall(msg.encode(FORMAT))
        if checksignup == False :
            conn.recv(1024)
            conn.sendall(msg2.encode(FORMAT))
            conn.recv(1024)

    # print("client address:",addr,"finished")
    # conn.close()



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST,SERVER_PORT))
s.listen()
print("SERVER SIDE")
print("server: ", HOST, SERVER_PORT)
print("Waiting for Client")
nClient = 0
while (nClient < 2):
    nClient += 1   
    try:
        conn, addr = s.accept()
        print("client address:",addr)
        print("conn:",conn.getsockname())
        tr = threading.Thread(target = handleClient,args=(conn,addr))
        tr.daemon = True
        tr.start()
    except:
        print("error")
s.close()