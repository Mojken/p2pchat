#!/usr/bin/env python3
import tty, sys, termios, os, threading, time
import networking, rendering, rendering

# Save terminal settings
orig_settings = termios.tcgetattr(sys.stdin)

class rendering_data():
    def __init__(self):
        self.view = "chat"
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
                frame.chat_view(data.mode, data.current_input)

            # clear
            os.system('clear')
            # draw
            print(frame, end="")
    os.system('clear')

def input_loop(data):
    tty.setcbreak(sys.stdin)
    print("\x1b[?25l")
    while data.running:
        data.mode = ""
        try:
            char = sys.stdin.read(1)[0]
            if char in handlers:
                handlers[char](data)
        except:
            stop(data)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
            exit()

data = rendering_data()
render_thread = threading.Thread(target=render, daemon=True, name="render", args=(data,))

# Start:
data.running = True
render_thread.start()
input_loop(data)
