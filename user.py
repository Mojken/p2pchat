#!/usr/bin/env python3
from json_database import JsonStorage
import os
import cryptography

data = JsonStorage("data.json")
contacts = []

class user:
    filename = "user.data"
    signer = None
    decrypt_cipher = None
    key = None
    chats = None
    username = ""

    def __init__(self):
        None

    def retrieve(self):
        self.filename = self.username + ".data"
        if not os.path.isfile(self.filename):
            return False
        cryptography.get_data(self)
        return True

    def create(self):
        self.filename = self.username + ".data"
        if os.path.isfile(self.filename):
            return False
        self.key = cryptography.generate_key(self.passphrase)
        self.chats = {0: {"name": self.username, "status": "online", "ip": "localhost", "chatlog": ["test", "test 2"]}}
        cryptography.setup_user(self)
        self.save()
        return True

    def save(self):
        cryptography.save_data(self)

    def add_contact(self, key, name, ip):
        exported_key = key.export_key()
        if exported_key not in chats:
            self.chats[exported_key] = {"name": name, "status": status, "ip": ip, "chatlog": []}
