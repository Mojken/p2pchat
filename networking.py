#!/usr/bin/env python3
import time, socket, threading, random

incoming_port = 1337

peers = []

class PeerHandler:
    def __init__(self, socket=None, address=None):
        if socket:
            self.socket = socket
        else:
            if address:
                outgoing_port = 65000+random.randint(1, 500)
                print("Opening socket to {}:{}".format(address, outgoing_port))
                self.socket = socket.socket()
                self.socket.connect((address, outgoing_port))
            else:
                raise

        self.outgoing = []
        self.incoming = []
        self.loop = False

    def listener(self):
        print("listening to incomming messages")
        while self.loop:
            self.incoming.append(self.socket.recv(4096).decode('utf-8'))

    def sender(self):
        while self.loop:
            if self.queue:
                print("sending")
                self.send_socket.send(self.outgoing.pop().encode('utf-8'))

    def start(self):
        sender = threading.Thread(target=self.sender)
        listener = threading.Thread(target=self.listener)

        self.loop = True

        listener.start()
        #sender.start()

    def disconnect():
        this.loop = False

def connection_listener():
    soc = socket.socket()
    soc.bind(('', incoming_port))
    soc.listen()

    loop = True
    while loop:
        (peer, address) = soc.accept()
        peer.settimeout(None)
        print("Connection from {}".format(address))
        peers.append(PeerHandler(peer, outgoing).start())

connection_listener_thread = threading.Thread(target=connection_listener)
connection_listener_thread.start()

def connect(address):
    print("Connecting...")
    peers.append(PeerHandler(address=address))
