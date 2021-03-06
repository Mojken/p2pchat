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
        self.connected = False
        self.encrypt_cipher = None

        if soc:
            self.soc = soc
            self.ip = soc.getpeername()[0]
            self.connected = True
        else:
            if address:
                print("Opening socket to {}:{}".format(address, incoming_port))
                self.ip = address
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
        try:
            pub_key_message = self.soc.recv(4096)
            self.encrypt_cipher = cryptography.get_encrypt_cipher(pub_key_message)
            self.verifier = cryptography.get_verifier(pub_key_message)

            ciphertext = self.soc.recv(4096)
            signature = cryptography.decrypt(self.soc.recv(4096))
            authentic = cryptography.verify_signature(signature, ciphertext, self.verifier)

            if authentic:
                print("Verified!")
            else:
                print("Not verified! Shutting down connection.")
                self.loop = False
                self.disconnect()

            self.soc.settimeout(0.0)
            while self.connected:
                ciphertext = self.soc.recv(4096)

                if not ciphertext:
                    continue

                try:
                    text = cryptography.decrypt(ciphertext).decode('utf-8')
                except:
                    if ciphertext == b'':
                        self.disconnect()
                        return
                    else:
                        text = ciphertext

                self.incoming.append(text)
                print(text) #Temporary
        except ConnectionResetError:
            print("Connection reset")
            self.disconnect()
        except OSError:
            print("An error arose, connection closed.")
            self.disconnect()
        except ValueError:
            print("An error arose, connection closed.")
            self.disconnect()

    def sender(self):
        pub_key = cryptography.get_key().publickey().exportKey(format='DER')
        self.soc.send(pub_key)

        signature = str(time.time()).encode('utf-8')

        self.soc.send(cryptography.sign_signature(signature))

        while not self.encrypt_cipher:
            None

        self.soc.send(cryptography.encrypt(signature, self.encrypt_cipher))

        while self.connected:
            if self.outgoing and self.encrypt_cipher:
                text = self.outgoing.pop().encode('utf-8')
                ciphertext = cryptography.encrypt(text, self.encrypt_cipher)
                self.soc.send(ciphertext)

    def start(self):
        if not self.connected:
            return

        sender = threading.Thread(target=self.sender, daemon=True, name="{} sender".format(self.ip))
        listener = threading.Thread(target=self.listener, daemon=True, name="{} listener".format(self.ip))

        listener.start()
        sender.start()

    def disconnect(self):
        print("Closing connection")
        global connected_ips
        if self.ip in connected_ips:
            connected_ips.remove(self.ip)

        self.soc.shutdown(socket.SHUT_RDWR) #Shut down, don't allow further send or recieves
        self.soc.close()
        self.connected = False

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
        if peer.connected:
            peers.append(peer)
            peer.start()
            connected_ips.append(address[0])

    soc.shutdown(socket.SHUT_RDWR)
    soc.close()

connection_listener_thread = threading.Thread(target=connection_listener, daemon=True, name="Connection Listener")
connection_listener_thread.start()

def connect(address):
    if address in connected_ips:
        print("Already connected!")
        return
    peer = PeerHandler(address=address)
    if peer.connected:
        peers.append(peer)
        peer.start()

        connected_ips.append(address)

def disconnect_all():
    for peer in peers:
        peer.disconnect()

def send_to_all(message):
    for peer in peers:
        peer.outgoing.append(message)
