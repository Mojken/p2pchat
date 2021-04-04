#!/usr/bin/env python3
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import os

decrypt_cipher = None

def generate_key():
    key = RSA.generate(2048)
    f = open('key.pem','wb')
    f.write(key.export_key('PEM'))
    f.close()

def get_key():
    global key
    f = open('key.pem', 'r')
    return RSA.import_key(f.read())

def get_encrypt_cipher(public_key):
    return PKCS1_OAEP.new(public_key)

def encrypt(message, decrypt_cipher):
    return encrypt_cipher.encrypt(message)

def decrypt(ciphertext):
    global decrypt_cipher
    if not decrypt_cipher:
        decrypt_cipher = PKCS1_OAEP.new(get_key())
    return decrypt_cipher.decrypt(ciphertext)
