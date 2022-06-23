import socket

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"
LIST = "list"
LOGIN = "login"
def sendList(client,list):
    for item in list:
        client.sendall(item.encode(FORMAT))
        client.recv(1024)
    msg = "end"
    client.sendall(msg.encode(FORMAT))

# def clientlogin(client):
#     account = []
#     username = input('username: ')
#     password = input('password: ')

#     #check username and password validation

#     account.append(username)
#     account.append(password)

#     # send account to server
#     sendList(client, account)
#     msg = client.recv(1024).decode(FORMAT)
#     print(msg)


def handleSever(client):
    msg = None
    msg2 = None
    list = ["anhtuan3536", "36", "45kg"]
    while(msg != "x" ):
        msg = input("talk: ")
        client.sendall(msg.encode(FORMAT))
        if(msg == LIST):
            client.recv(1024)
            sendList(client,list)
        # if(msg == LOGIN):
        #     client.recv(1024)
        #     clientlogin(client)
        # msg2 = client.recv(1024).decode(FORMAT)
        # print("server respond:",msg2)
        # if(msg2 == "x" or msg == "x"):
        #     break


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    print("CLIENT SIDE")
    client.connect( (HOST, SERVER_PORT) )
    print("client address:", client.getsockname())
    handleSever(client)

except:
    print("error")