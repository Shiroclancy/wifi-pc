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
with open("accounts.json","r") as f:
    content = json.load(f)

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
    while(True):
        msg = conn.recv(1024).decode(FORMAT)
        while(msg != INVALID and msg != SUCCESS):
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
            if(msg == SIGNUP):
                account = {"username": username, "password" : password}
                content.append(account)
                with open("accounts.json","w") as f:
                    json.dump(content,f,indent=2)
                msg = SUCCESS
        conn.sendall(msg.encode(FORMAT))
    # print("client address:",addr,"finished")
    # conn.close()



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
        tr = threading.Thread(target = handleClient,args=(conn,addr))
        tr.daemon = True
        tr.start()
    except:
        print("error")
s.close()