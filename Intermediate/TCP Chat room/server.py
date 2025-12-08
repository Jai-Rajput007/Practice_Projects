import socket
import threading

class Server:
    
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.clients = []
        self.client_lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        self.server_socket.bind((host,port))
        print(f"Sever bound to {self.host}:{self.port}")
    
    def start(self):
        self.server_socket.listen(1)
        print(f"Server is listening..... and running on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Client is connected with id {addr}")
        
            clients_thread = threading.Thread(target=self.handle_client,args=(client_socket,addr))
            clients_thread.start()
    
    def handle_client(self,client_socket,address):
        print(f"New thread started for {address}")
        with self.client_lock:
            self.clients.append(client_socket)
        try:
            welcome_message = f"Welcome, client{address},You are connected\r\n"
            client_socket.send(welcome_message.encode('utf-8'))
            while True:
             data = client_socket.recv(1024)
             if not data:
                 break
             message = data.decode('utf-8').strip()
             broadcast_message = f"Client {address}: {message}"
             self.broadcast(broadcast_message,client_socket)

        except Exception as e:
            print(f"Error with client {address}:{e}")
        
        finally:
            self.remove_client(client_socket,address)
    
    def broadcast(self,message,sender_socket):
        

    def remove_client(self,client_socket):
            with self.client_lock:
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
            left = f"User {client_socket} left the chat"
            self.broadcast(left,client_socket)
            client_socket.close()
        