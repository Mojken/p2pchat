#!/usr/bin/env python3
import tty, sys, termios, os, threading, time
import networking, rendering, rendering, user
import cryptography

# Save terminal settings
orig_settings = termios.tcgetattr(sys.stdin)

# This should be a dict
class rendering_data():
    def __init__(self):
        self.user = user.user()
        self.view = "login"
        self.mode = ""
        self.current_input = ""
        self.running = False
        self.input_mode = True

def toggle_input_mode(data):
    if data.input_mode:
        tty.setcbreak(sys.stdin)
    else:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)

    data.input_mode = not data.input_mode

def input_text(data):
    data.current_input = ""
    while True:
        char = sys.stdin.read(1)[0]
        if char is '\x1b': #Escape
            data.current_input = ""
            return False
        elif char is '\n': #Enter
            return True
        elif char is '\x7f': #Backspace
            data.current_input = data.current_input[:-1]
        else:
            data.current_input += char

def insert(data):
    data.mode = "INSERT"
    while input_text(data):
        #networking.send_to_all(message)
        None

def connect(data):
    data.mode = "connect"
    if input_text(data):
        address = data.current_input
        networking.connect(address)

def stop(data):
    data.running = False
    networking.disconnect_all()
    print("\033[m")     # Reset colour
    print("\x1b[?25h")  # Show cursor
    os.system('clear')  # Clear screen
    # Reset terminal settings
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    exit()

handlers = {
    'i': insert,
    'c': connect,
    'q': stop
}

def render(data):
    timestamp = 0
    while data.running:
        if time.time() >= timestamp + 1/30:
            timestamp = time.time()

            # process
            frame = rendering.frame()

            if data.view is "chat":
                frame.chat_view(data.mode, data.current_input, list(data.user.chats.values()))
            if data.view is "login":
                if data.user:
                    frame.login_view(mode=data.mode, username=data.user.username, current_input=data.current_input)

            # clear
            #os.system('clear')
            # draw
            print(frame, end="")
    os.system('clear')

def input_loop(data):
    tty.setcbreak(sys.stdin)
    print("\x1b[?25l") # Hide cursor
    while data.running:
        data.mode = ""
        try:
            char = sys.stdin.read(1)[0]
            if char in handlers:
                handlers[char](data)
        except:
            stop(data)

def login_loop(data):
    tty.setcbreak(sys.stdin)
    print("\x1b[?25l") # Hide cursor
    while True:
        data.mode = "username"
        input_text(data)
        data.user.username = data.current_input
        data.mode = "passphrase"
        input_text(data)
        data.user.passphrase = data.current_input
        if login(data.user):
            break
    data.mode = ""

def login(user):
    if user.retrieve():
        return True
    else:
        data.mode = "failed"
        char = None
        while True:
            char = sys.stdin.read(1)[0]
            if char in ["t", "c", "q"]:
                break
        if char is "t":
            return False
        if char is "c":
            data.mode = "create"
            input_text(data)
            if user.passphrase == data.current_input:
                user.create()
            return True
        if char is "q":
            stop(data)

data = rendering_data()
render_thread = threading.Thread(target=render, daemon=True, name="render", args=(data,))

# Start:
data.running = True
render_thread.start()
#login_loop(data)
data.user.username = "Mojken"
data.user.passphrase = "645am"
data.user.retrieve()
data.view = "chat"
input_loop(data)
