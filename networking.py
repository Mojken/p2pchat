#!/usr/bin/env python3
import time, socket, threading, random

incoming_port = 1337

peers = []

random.seed()
class PeerHandler:
    def __init__(self, soc=None, address=None):
        self.outgoing = []
        self.incoming = []
        self.loop = False
        self.connected = False

        if soc:
            self.soc = soc
        else:
            if address:
                outgoing_port = 65000+random.randint(1, 500)
                print("Opening socket to {}:{}".format(address, outgoing_port))
                self.soc = socket.socket()
                try:
                    print("Trying to connect...")
                    self.soc.connect((address, incoming_port))
                    self.connected = True
                except:
                    print("Failed to connect!")
                    return
                print("Connected!")
            else:
                raise


    def listener(self):
        print("listening to incomming messages")
        while self.loop:
            message = self.soc.recv(4096).decode('utf-8')
            self.incoming.append(message)
            print(message)

    def sender(self):
        while self.loop:
            if self.outgoing:
                print("sending")
                self.soc.send(self.outgoing.pop().encode('utf-8'))

    def start(self):
        if not self.connected:
            return

        sender = threading.Thread(target=self.sender)
        listener = threading.Thread(target=self.listener)

        self.loop = True

        listener.start()
        sender.start()

    def disconnect():
        this.loop = False

loop = False
def connection_listener():
    soc = socket.socket()
    soc.bind(('', incoming_port))
    soc.listen()

    global loop
    loop = True
    while loop:
        (peer, address) = soc.accept()
        peer.settimeout(None)
        print("Connection from {}".format(address))
        peer = PeerHandler(soc=peer)
        peers.append(peer)
        peer.start()

connection_listener_thread = threading.Thread(target=connection_listener)
connection_listener_thread.start()

def connect(address):
    peer = PeerHandler(address=address)
    peers.append(peer)
    peer.start()

def disconnect_all():
    for peer in peers:
        peer.disconnect()
    connection_listener_thread.stop()
