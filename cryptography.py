#!/usr/bin/env python3
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA512
from Crypto.Signature import PKCS1_PSS
import os, codecs, time

def generate_key(passphrase):
    for i in range(3):
        key = RSA.generate(2048)
        if test(key, passphrase):
            return key
    return None

def test(key, passphrase):
    try:
        keybytes = key.exportKey(format="DER", passphrase=passphrase)
        err = 1200 - len(keybytes)
        keybytes += err.to_bytes(1, 'little') * err

        padding = int.from_bytes(keybytes[-2:-1], 'little')
        padding = keybytes[-2:-1] * padding
        if keybytes.endswith(padding):
            keybytes = keybytes[:-len(padding)]
            RSA.importKey(keybytes, passphrase)
        return True
    except:
        return False

# Private-key methods:

def get_data(user):
    if not os.path.isfile(user.filename):
        return False
    with open(user.filename, 'rb') as f:
        dec = codecs.getincrementaldecoder('utf-8')()
        savedata = f.read()

        keybytes = savedata[0:1200]
        padding = int.from_bytes(keybytes[-2:-1], 'little')
        padding = keybytes[-2:-1] * padding
        if keybytes.endswith(padding):
            keybytes = keybytes[:-len(padding)]
        else:
            raise ValueError("Data corrupted, couldn't find private key")

        key = None
        savefile_encrypted = None
        user.key = RSA.importKey(keybytes, user.passphrase)
        savefile_encrypted = savedata[1200:]
        setup_user(user)
        user.chats = eval(decrypt(user, savefile_encrypted).decode("utf-8"))

def setup_user(user):
    user.signer = PKCS1_PSS.new(user.key)
    user.decrypt_cipher = PKCS1_OAEP.new(user.key)

def decrypt(user, ciphertext):
    return user.decrypt_cipher.decrypt(ciphertext)

def sign_signature(user, signature):
    h = SHA512.new(signature)
    return user.signer.sign(h)

def save_data(user):
    with open(user.filename, 'wb') as f:
        keybytes = user.key.exportKey(format="DER", passphrase=user.passphrase)
        err = 1200 - len(keybytes)
        keybytes += err.to_bytes(1, 'little') * err

        f.write(keybytes + encrypt(repr(user.chats).encode("utf-8"), user.decrypt_cipher))

# Public-key methods:

def get_verifier(public_key):
    return PKCS1_PSS.new(RSA.importKey(public_key))

def verify_signature(signature, message, verifier):
    h = SHA512.new(signature)
    try:
        verifier.verify(h, message)
        return True
    except (ValueError, TypeError):
        return False

def get_encrypt_cipher(public_key):
    return PKCS1_OAEP.new(RSA.importKey(public_key))

def encrypt(message, encrypt_cipher):
    return encrypt_cipher.encrypt(message)
