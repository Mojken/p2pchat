#!/usr/bin/env python3
import tty, sys, termios

# Save terminal settings
orig_settings = termios.tcgetattr(sys.stdin)

tty.setcbreak(sys.stdin)
print(sys.stdin.read(1)[0])

# Reset terminal settings to original
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
