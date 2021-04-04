import time, socket, threading

port = 1337

recieve_socket = socket.socket()
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
recieve_socket.bind((host_name, port))

print(host_name, '({})'.format(ip))

incomming = []
outgoing = []

class ConnectionHandler:
    def __init__(self, recieve_socket, address):
        self.recieve_socket = recieve_socket
        self.address = address # (address, port)

    def listener(self, queue):
        self.socket.listen()
        loop = True
        while loop:
            message = self.recieve_socket.recv(4096)
            print(message)

    def sender(self, queue):
        loop = True
        while loop:
            if queue:
                print("sending")
                self.send_socket.send(queue.pop())

    def start(self):
        self.send_socket = socket.create_connection(self.address)

        listener = threading.Thread(target=self.listener, args=(incomming,))
        sender = threading.Thread(target=self.sender, args=(outgoing,))

        listener.start()
        sender.start()

port = input("port: ")
ConnectionHandler(recieve_socket, ("127.0.1.1", port)).start()

while True:
    outgoing.append(input("> "))
