import socket
import threading
import re
import queue
import time
import ast
import msvcrt

# get public ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
s.close()

Spare_PORT = 50007 

posts = [
    "hello", 
    "my messages",
    "are",
    "here"
    ]

blacklist = ['172.31.15.183']

trusts = [HOST]

def make_server_socket(PORT):
    # initialize server socket
    global HOST
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("SERVER: HOST: ", HOST, "is listening on PORT:", PORT)
        s.bind((HOST, PORT))
        s.listen(5)
        conn, addr = s.accept() 
        with conn:
            #print(addr[0], type(addr))
            #if addr[0] in blacklist:
            #    s.shutdown()
            print("SERVER: Connected by", addr)
            ack_message = "CONN_ESTBLD"
            conn.sendall(ack_message.encode())
            if conn.recv(1024) != "ACK":
                conn.settimeout(0)
            
            while True:
                conn.setblocking(1)
                data = conn.recv(1024).decode()
                print("SERVER: Received:", data, "from", addr)
                if not data:
                    conn.sendall("END".encode())
                    print("SERVER: connection terminated")
                    break
                if re.search(r"\\find:.*", data):
                    if len(re.search(r"\\find:.*", data).group()) > 6:
                        trust_list = ast.literal_eval(conn.recv(1024).decode())
                        print("SERVER: Received:", trust_list, "from", addr)
                        search_result = "FOUND:"+str(find(data[6:], trust_list))
                        print("SERVER:", search_result, "for CLIENT ", addr)
                        conn.sendall(search_result.encode())    # send stringified list of results
                else:
                    invalid_alert = "INVALID DATA RECEIVED: "+data
                    conn.sendall(invalid_alert.encode())
                

def make_client_socket(HOST):
    State = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, 50007))
    print("CLIENT: Connected to :", HOST)
    trusts.append(HOST)
    while True:
        if State == 0:
            PORT = int(s.recv(1024).decode())
            print("SERVER : -> ",PORT)
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            print("State 1")
            State = 1
        if State == 1:
            
            data = s.recv(1024).decode()
            print("CLIENT: Received:", data, "from", HOST)
            if data == "CONN_ESTBLD":
                State = 2
                s.sendall("ACK".encode())
        elif State == 2:
            user_input = input("CLIENT: Choose : 1 - Chat\n2 - Find\n")         
            if user_input == '1':
                State = 4
            elif user_input == '2':
                State = 3
        elif State == 3:
            print("Enter word to search:\n")
            msg = input('')
            if msg:
                find_request ="\\find:"+msg
                s.sendall(find_request.encode())
                s.sendall(str(trusts).encode())
                print("CLIENT : SERVER :"+str(s.recv(4096).decode()))
                State = 2
        elif State == 4:
            print("Enter \\end to end Connection")
            print("Enter \\find to start a Search")
            while True:
                print("Enter Message:\n")
                msg = input("")
                if msg == "\\end":
                    State = -1
                    break
                elif msg == "\\find":
                    State = 3
                else:
                    s.sendall(msg.encode())
                    print("CLIENT: Received:",s.recv(4096).decode(), "from", HOST)
                           
        else:
            break
    print("CLIENT: CONNECTION TERMINATED")
    s.close()


def server_service(PORT=Spare_PORT):
    # initialize server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("SERVER: HOST: ", HOST, "is listening on PORT:", PORT)
        s.bind((HOST, PORT))
        global Spare_PORT
        while True:
            s.listen(5)
            conn, addr = s.accept() 
            with conn:
                Spare_PORT += 1
                threading.Thread(target=make_server_socket, args=(Spare_PORT,)).start() 
                conn.sendall(str(Spare_PORT).encode())
                conn.settimeout(0)


def client_service():
    while True:        
        print("CLIENT : Select : ")
        print("CLIENT : 1 - Trust List ")
        print("CLIENT : 2 - Posts ")
        print("CLIENT : 3 - Add Post ")
        print("CLIENT : 4 - Connect to Peer ")
        print("CLIENT : 5 - Add to BLACKLIST")
        print("CLIENT : 6 - BLACKLIST CHECK")
        print("Choose one of the above : ")
        user_input = input()
        if user_input == "1":
            for trust in (trusts):
                print("CLIENT :", trust)
        elif user_input == "2":
            for post in (posts):
                print("CLIENT :", post)
        elif user_input == "3":
            new_post = input("CLIENT : Enter New Post\n")
            posts.append(new_post)
        elif user_input == "4":
            print("CLIENT : BEGIN")
            user_input = input("CLIENT : Enter HOST IP\n")
            newThread = threading.Thread(target=make_client_socket,args=(user_input,))
            newThread.start()
            newThread.join()
        elif user_input == "5":
            print("Enter IP :")
            input_ = input('')
            blacklist.append(input_)
        elif user_input == "6":
            for address in blacklist:
                print("CLIENT :", address)
        else:
            print("TRY AGAIN")

def find(data, trust_list):
    
    global HOST

    search_result = []
    
    for post in posts:
        if data in post:
            search_result.append(post)
        
    for host in trusts:
        if host != HOST and host not in trust_list:
            result_queue = queue.Queue()
            threading.Thread(target=searching_client, args=(host, data, trust_list.append(trusts), result_queue)).start().join()
            result = result_queue.get()
            for result in result_queue.get():
                if result not in search_result:
                        search_result.append(result)

    return search_result
    

def searching_client(HOST, msg, trust_list, result_queue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, 50007))
    print("CLIENT: Connected to", HOST)
    PORT = int(s.recv(1024).decode())
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    data = s.recv(1024).decode()
    if data == "CONN_ESTBLD":
        s.sendall("ACK".encode())
        find_request = "\\find:"+msg
        s.sendall(find_request.encode())
        trust_list = ''.join(trust_list)
        s.sendall(trust_list)
        data = s.recv(4096).decode()
        print("CLINET: Received", data, "from", HOST)
        result_queue.put(ast.literal_eval(data))
    else:
        s.close()

if __name__ == "__main__":
    client_thread = threading.Thread(target=client_service).start()
    server_thread = threading.Thread(target=server_service).start()
    
