#!/usr/bin/env python3
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_PSS
import os

decrypt_cipher = None
signer = None

def generate_key():
    if os.path.isfile('key.pem'):
        return get_key()

    key = RSA.generate(2048)
    f = open('key.pem','wb')
    f.write(key.exportKey('PEM'))
    f.close()
    return key

def get_key():
    if not os.path.isfile('key.pem'):
        return generate_key()
    f = open('key.pem', 'r')
    return RSA.importKey(f.read())

def get_encrypt_cipher(public_key):
    return PKCS1_OAEP.new(RSA.importKey(public_key))

def encrypt(message, encrypt_cipher):
    return encrypt_cipher.encrypt(message)

def decrypt(ciphertext):
    global decrypt_cipher
    if not decrypt_cipher:
        decrypt_cipher = PKCS1_OAEP.new(get_key())
    return decrypt_cipher.decrypt(ciphertext)

def sign_signature(signature):
    global signer
    if not signer:
        key = get_key()
        signer = PKCS1_PSS.new(key)

    h = SHA256.new(signature)
    return signer.sign(h)

def get_verifier(public_key):
    return PKCS1_PSS.new(public_key)

def verify_signature(signature, message, verifier):
    h = SHA256.new(signature)
    try:
        verifier.verify(h, message)
        return True
    except (ValueError, TypeError):
        return False
