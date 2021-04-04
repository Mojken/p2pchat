import time, socket, threading

port = 1337
outgoing = []
incoming = []

class PeerHandler:
    def __init__(self, socket, queue):
        self.socket = socket
        self.queue = queue
        self.loop = False

    def listener(self):
        #upload_port_num = 65000+random.randint(1, 500)
        while self.loop:
            print(self.socket.recv(4096).decode('utf-8'))

    def sender(self):
        while self.loop:
            if self.queue:
                print("sending")
                self.send_socket.send(self.queue.pop())

    def start(self):
        sender = threading.Thread(target=self.sender)
        listener = threading.Thread(target=self.listener)

        self.loop = True

        listener.start()
        #sender.start()

def connection_listener():
    soc = socket.socket()
    soc.bind(('', port))
    soc.listen()

    loop = True
    while loop:
        (peer, address) = soc.accept()
        peer.settimeout(None)
        print("Connection from {}".format(address))
        PeerHandler(peer, outgoing).start()

connection_listener_thread = threading.Thread(target=connection_listener)
connection_listener_thread.start()

peer_soc = socket.socket()
peer_soc.connect((input("IP: "), port))

while True:
    try:
        peer_soc.send(input("> ").encode('utf-8'))
    except KeyboardInterrupt:
        raise
