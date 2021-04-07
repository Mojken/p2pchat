#!/usr/bin/env python3
import os, math, textwrap

lines = {
    5: u"\u2577",
    6: u"\u2576",
    7: u"\u250C",
    12: u"\u2574",
    13: u"\u2510",
    14: u"\u2500",
    15: u"\u252C",
    20: u"\u2575",
    21: u"\u2502",
    22: u"\u2514",
    23: u"\u251C",
    28: u"\u2518",
    29: u"\u2524",
    30: u"\u2534",
    31: u"\u253C",
}


class frame():
    def __init__(self):
        self.sidebar_width = 16
        self.input_height = 1
        self.size = os.get_terminal_size()
        self.pixels = []
        self.pixels_rendered = []
        self.data = {
            "active chat": 0,
            "contacts": [
                {
                    "name": "Thure",
                    "chatlog": ["Thure: Hello!", "Mojken: Hi! <3", "Thure: That porn you sent me last time was super hot, wud you mind sending me some more? I don't have a lot of time to watch it since Thea is always aronud, but every now and then I want to be able to check some out.", "Mojken: lol"],
                    "status": "online"
                },
                {
                    "name": "Oatmealongname this is a really, really long name",
                    "chatlog": [],
                    "status": "offline"
                }
            ]
        }
        self.wrapper = textwrap.TextWrapper(expand_tabs=True, tabsize=4, drop_whitespace=True, break_on_hyphens=True, width=self.size.columns - self.sidebar_width - 3)

        for x in range(self.size.lines):
            self.pixels.append([])
            self.pixels_rendered.append([])
            for y in range(self.size.columns):
                self.pixels[x].append(0)
                self.pixels_rendered[x].append(" ")

    def chat_view(self, mode, current_input):
        self.input_height = min(max(round(len(current_input) / (self.size.columns - self.sidebar_width - 2) + 0.5) + 2, 5), self.size.lines-10)

        #lines
        for x in range(self.size.lines):
            for y in range(self.size.columns):
                if y is self.sidebar_width:
                    self.pixels[x][y] = 1
                if x is self.size.lines - self.input_height and y > self.sidebar_width:
                    self.pixels[x][y] = 1
                if x is 0 or y is 0 or x is self.size.lines - 1 or y is self.size.columns - 1:
                    self.pixels[x][y] = 1

        self.post_processing()

        #contacts
        xb = 0
        yb = 0
        for xa in range(1, self.size.lines - 1):
            if xb < len(self.data["contacts"]):
                for ya in range(1, self.sidebar_width - 1):
                    colour = "\033["
                    if self.data["contacts"][xb]["status"] is "online":
                        colour += "32"
                    elif self.data["contacts"][xb]["status"] is "offline":
                        colour += "38"
                    if xb is self.data["active chat"]:
                        colour += ";40"
                    colour += "m"
                    if yb < len(self.data["contacts"][xb]["name"]):

                        text = self.data["contacts"][xb]["name"][yb]

                        if yb is 0:
                            text = colour + text

                        self.pixels_rendered[xa][ya] = text
                        yb += 1
                    if ya is self.sidebar_width - 2:
                        self.pixels_rendered[xa][ya] += "\033[m"
                xb += 1
                yb = 0

        #chatlog
        xb = 0
        yb = 0
        newline = False
        for xa in range(1, self.size.lines - self.input_height):
            for ya in range(self.sidebar_width + 1, self.size.columns - 1):
                active_chat = self.data["contacts"][self.data["active chat"]]["chatlog"]
                if xb < len(active_chat):
                    active_chat = self.wrapper.fill(active_chat[xb])
                    if yb < len(active_chat):
                        if active_chat[yb] is "\n":
                            yb += 1
                            newline = True
                            break
                        self.pixels_rendered[xa][ya] = active_chat[yb]
                        yb += 1
                    else:
                        newline = False
            if not newline:
                xb += 1
                yb = 0

        for y in range(len(mode)):
            self.pixels_rendered[self.size.lines-1][y+self.sidebar_width+2] = mode[y]

        for y in range(len(self.data["contacts"][self.data["active chat"]]["name"])):
            self.pixels_rendered[0][y+self.sidebar_width+2] = self.data["contacts"][self.data["active chat"]]["name"][y]

        if mode is "INSERT":
            current_input = self.wrapper.fill(current_input + u"\u2589")
            yb = 0
            for xa in range(self.size.lines - self.input_height + 1, self.size.lines - 1):
                for ya in range(self.sidebar_width + 1, self.size.columns - 1):
                    if yb < len(current_input):
                        if current_input[yb] is "\n":
                            yb += 1
                            xb += 1
                        self.pixels_rendered[xa][ya] = current_input[yb]
                        yb += 1
                if yb >= len(current_input):
                    break

    def popup(self, title, text):
        width = max(len(title) + 3, math.sqrt(len(text))*16/9)

        self.wrapper.width = width
        lines = self.wrapper.wrap(text)
        text = "\n".join(lines)
        height = round(len(lines)) + 2

        start_x = round((self.size.lines - height)/2)
        end_x = self.size.lines
        start_y = round((self.size.columns - width)/2)
        end_y = round((self.size.columns + width)/2) + 2

        width = end_y - start_y

        xb = 0
        yb = 0
        done = False
        for xa in range(start_x, end_x):
            for ya in range(start_y, end_y + 1):
                if yb < len(text):
                    if text[yb] is "\n":
                        xb += 1
                        yb += 1
                        break
                    self.pixels_rendered[xa][ya] = text[yb]
                else:
                    end_x = xa+1
                    height = end_x - start_x
                    done = True
                    break
                yb += 1
            if done:
                break
            xb += 1

        xb = 0
        yb = 0
        for xa in range(max(0, start_x - 1), min(end_x + 1, self.size.lines)):
            for ya in range(start_y - 1, end_y + 1):
                if xb is 0 or yb is 0 or xb is height + 1 or yb is width + 1:
                    self.pixels[xa][ya] = 1
                yb += 1
            xb += 1
            yb = 0

        self.post_processing()

        for x in range(len(title)):
            self.pixels_rendered[start_x - 1][start_y + 1 + x] = title[x]

    def post_processing(self):
        for x in range(self.size.lines):
            for y in range(self.size.columns):
                line_type = 0

                if x > 0:
                    line_type += self.pixels[x-1][y]
                line_type *= 2

                if y > 0:
                    line_type += self.pixels[x][y-1]
                line_type *= 2

                line_type += self.pixels[x][y]
                line_type *= 2

                if y < self.size.columns - 1:
                    line_type += self.pixels[x][y+1]
                line_type *= 2

                if x < self.size.lines - 1:
                    line_type += self.pixels[x+1][y]

                if line_type in lines:
                    self.pixels_rendered[x][y] = lines[line_type]

        for x in range(self.size.lines):
            self.pixels[x] = []
            for y in range(self.size.columns):
                self.pixels[x].append(0)

        return self

    def __str__(self):
        frame_text = ""
        for row in self.pixels_rendered:
            for char in row:
                frame_text += char
        return frame_text
