from queue import Empty
import socket
import threading
import pyodbc
HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"

LIST = 'list'
LOGIN = 'login'


def recvList(conn):
    list = []
    item = conn.recv(1024).decode(FORMAT)
    while(item != "end"):
        list.append(item)
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    return list

# def serverLogin(conn):
#     user = recvList(conn)
#     cursor.execute("select pass from Account where username = ?", user[0])
#     password = cursor.fetchone()
#     msg = "Invalid"
#     if(password is None):
#         msg = "Invalid"
#         print(msg)
#     else:
#         userPassword = password[0]
#         if(userPassword == user[1]):
#             msg = "login successfully"
#             print(msg)
#     conn.sendall(msg.encode(FORMAT))


def handleClient(conn, addr):
    msg = None
    msg2 = None
    while(msg != "x"):
        msg = conn.recv(1024).decode(FORMAT)
        print("client",addr,"talk:",msg)
        if(msg == LIST):
            conn.sendall(msg.encode(FORMAT))
            list = recvList(conn)
            print("recieved")
            a = 0
            for item in list:
                a+=1
                if(a == 1):
                    print("username:", item)
                if(a == 2):
                    print("height:", item)
                if(a == 3):
                    print("weight:", item)

        # if(msg == LOGIN):
        #     conn.sendall(msg.encode(FORMAT))
        #     serverLogin(conn)
        if(msg == "x"):
            break
        # msg2 = input("respond: ")
        # conn.sendall(msg2.encode(FORMAT))
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
        tr = threading.Thread(target = handleClient,args=(conn,addr))
        tr.daemon = True
        tr.start()
    except:
        print("error")
s.close()