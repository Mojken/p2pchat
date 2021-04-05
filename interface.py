#!/usr/bin/env python3
import tty, sys, termios, networking

# Save terminal settings
orig_settings = termios.tcgetattr(sys.stdin)

mode = True
def toggle_input_mode():
    global mode
    if mode:
        tty.setcbreak(sys.stdin)
    else:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)

    mode = not mode

def insert():
    toggle_input_mode()
    networking.send_to_all(input("> "))
    toggle_input_mode()

def connect():
    print("connect")
    toggle_input_mode()
    address = input("IP: ")
    networking.connect(address)
    toggle_input_mode()

def stop():
    global running
    running = False
    networking.disconnect_all()

handlers = {
    'i': insert,
    'c': connect,
    'q': stop
}

toggle_input_mode()
running = True
while running:
    try:
        char = sys.stdin.read(1)[0]
        if char in handlers:
            handlers[char]()
    except:
        stop()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
        exit()

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
