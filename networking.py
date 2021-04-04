#!/usr/bin/env python3
import time, socket, threading, random
import cryptography

incoming_port = 1337

peers = []
connected_ips = []

random.seed()
class PeerHandler:
    def __init__(self, soc=None, address=None):
        self.outgoing = []
        self.incoming = []
        self.loop = False
        self.connected = False

        if soc:
            self.soc = soc
            self.connected = True
        else:
            if address:
                print("Opening socket to {}:{}".format(address, incoming_port))
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
        public_key = cryptography.import_key(self.soc.recv(4096))
        self.encrypt_cipher = cryptography.get_encrypt_cipher(public_key)

        while self.loop:
            ciphertext = self.soc.recv(4096)
            text = cryptography.decrypt(ciphertext).decode('utf-8')
            self.incoming.append(text)
            print(text)

    def sender(self):
        key = cryptography.get_key().publickey().export_key(format='DER')
        self.soc.send(key)

        while self.loop:
            if self.outgoing:
                print("sending")
                text = self.outgoing.pop().encode('utf-8')
                ciphertext = cryptography.encrypt(text, self.encrypt_cipher)
                self.soc.send(ciphertext)

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
        (peer_soc, address) = soc.accept()
        peer_soc.settimeout(None)
        print("Connection from {}:{}".format(address[0], address[1]))
        peer = PeerHandler(soc=peer_soc)
        peers.append(peer)
        peer.start()

        connected_ips.append(address[0])

connection_listener_thread = threading.Thread(target=connection_listener)
connection_listener_thread.start()

def connect(address):
    if address in connected_ips:
        print("Already connected!")
        return
    peer = PeerHandler(address=address)
    peers.append(peer)
    peer.start()

    connected_ips.append(address)

def disconnect_all():
    for peer in peers:
        peer.disconnect()
    connection_listener_thread.stop()

def send_to_all(message):
    for peer in peers:
        peer.outgoing.append(message)
