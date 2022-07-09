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
FINDROOM = 'room information'
FINDROOMBOOK = 'room book'
monthDays= [ 31, 28, 31, 30, 31, 30,31, 31, 30, 31, 30, 31 ]
def countLeapYears(list):
   years = list[0]
   if (list[1] <= 2):
      years-=1
   return years/4 - years/100 +  years/400
def getDifference(list1, list2):
   n1 = list1[0] * 365 + list1[2]
   i = 0
   while i< list1[1]-1:
      n1 += monthDays[i]
      i+=1

   n1 += countLeapYears(list1)
   n2 = list2[0] * 365 + list2[2]
   j  = 0 
   while j< list2[1]-1:
      n2 += monthDays[j]
      j+=1
   n2 += countLeapYears(list2)
   return (n2 - n1)
def checkBookedDay(DateEntry1, DateLeaving1, DateEntry2, DateLeaving2):
    if(getDifference(DateEntry2,DateEntry1) >= 0 and getDifference(DateLeaving2,DateEntry1) < 0):
        return False
    if(getDifference(DateEntry2,DateLeaving1) > 0 and getDifference(DateLeaving2,DateLeaving1) <= 0):
        return False
    if(getDifference(DateEntry2,DateEntry1) <= 0 and getDifference(DateLeaving2,DateLeaving1) >= 0):
        return False
    return True
def checkBookedRoom(DateEntry, DateLeaving, Bookedroom):
    for clientBooked in Bookedroom["ListBookedClient"]:
        if(checkBookedDay(DateEntry, DateLeaving,clientBooked["DateEntry"],clientBooked["Date of leaving"]) == False):
            return False
    return True
def myFunc(ID):
    return ID
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
def recvListt(conn):
    list = []
    item = conn.recv(1024).decode(FORMAT)
    while(item != "end"):
        list.append(item)
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    return list
def handleLogin(msg,conn):
    acc = {}
    while(msg != INVALID and msg != SUCCESS):
        username = conn.recv(1024).decode(FORMAT)
        conn.sendall(username.encode(FORMAT))
        password = conn.recv(1024).decode(FORMAT)
        conn.sendall(password.encode(FORMAT))
        for cont in accounts:
            if cont['username'] == username and cont['password'] == password :
                acc = cont
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
        conn.recv(1024)
        conn.sendall(json.dumps(acc,indent=2).encode(FORMAT))
        conn.recv(1024)
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
def sendListRoomAvailable(conn,listId,IDhotel,listroom):
    for id in listId:
        listroom[id]['Price'] = hotel[IDhotel]['Price'][listroom[id]['TypeRoom']] + hotel[IDhotel]['Price'][listroom[id]['Bed']]
        rooom = listroom[id]
        conn.sendall(json.dumps(rooom,indent=2).encode(FORMAT))
        conn.recv(1024)
    msg = "end"
    conn.sendall(msg.encode(FORMAT))
def handleFindroomInfor(conn,ms):
    msg = 'ok'
    roomtype = None
    bedtype = None
    DateEntry = recvListt(conn)
    DateEntry = [int(i) for i in DateEntry]
    conn.sendall(msg.encode(FORMAT))
    DateLeaving = recvListt(conn)
    DateLeaving = [int(i) for i in DateLeaving]
    conn.sendall(msg.encode(FORMAT))
    indexHotel = conn.recv(1024).decode(FORMAT)
    conn.sendall(indexHotel.encode(FORMAT))
    if (ms == FINDROOMBOOK):
        roomtype = recvListt(conn)
        conn.sendall(msg.encode(FORMAT))
        bedtype = recvListt(conn)
        conn.sendall(msg.encode(FORMAT))
    if(indexHotel.isdigit() == True):
        indexHotel = int(indexHotel)
    else:
        for hot in hotel:
            if (str(indexHotel).upper() == hot['name']):
                indexHotel = hot['IDhotel']
    listId = []
    if (ms == FINDROOM):
        for room in hotel[indexHotel]['BlankRoom']:
            # print(json.dumps(hotel["Hotel"][int(Hotel)-1]['ListRoom'][room],indent=2))
            listId.append(room)
        for room in hotel[indexHotel]['Booked']:
            if(checkBookedRoom(DateEntry, DateLeaving, room)):
                # print(json.dumps(hotel["Hotel"][int(Hotel)-1]['ListRoom'][room["IDroom"]],indent=2))
                listId.append(room["IDroom"])
    else:
        for rom in roomtype:
            for be in bedtype:
                for room in hotel[indexHotel]['BlankRoom']:
                    if (room in hotel[indexHotel][rom] and room in hotel[indexHotel][be]):
                        listId.append(room)
        for rom in roomtype:
            for be in bedtype:
                for room in hotel[indexHotel]['Booked']:
                    if((room['IDroom'] in hotel[indexHotel][rom] and room['IDroom'] in hotel[indexHotel][be]) and checkBookedRoom(DateEntry, DateLeaving, room)):
                        # print(json.dumps(hotel["Hotel"][int(Hotel)-1]['ListRoom'][room["IDroom"]],indent=2))
                        listId.append(room["IDroom"])
    listId.sort()
    # listId = [str(i) for i in listId]
    # sendList(conn,listId)
    sendListRoomAvailable(conn,listId,indexHotel,hotel[indexHotel]['ListRoom'])
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
        if(msg == FINDROOM or msg == FINDROOMBOOK):
            handleFindroomInfor(conn,msg)
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