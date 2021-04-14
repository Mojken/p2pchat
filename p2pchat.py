#!/usr/bin/env python3
import tty, sys, termios, traceback

# Save terminal settings
orig_settings = termios.tcgetattr(sys.stdin)

try:
    import interface.py
except Exception as e:
    print("\033[m")     # Reset colour
    print("\x1b[?25h")  # Show cursor
    # Reset terminal settings
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    traceback.print_exc()
